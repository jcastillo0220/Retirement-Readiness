import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from google import genai

from generator import generate_suggestions
from cache import make_cache_key, cache_get, cache_set
from validation import parse_validation_json, build_repair_prompt
from scenario_engine import compute_projection

from chunking import retrieve_definition_chunks, retrieve_numeric_chunks
from citation_formatter import format_with_citations
from validation import validate_answer

load_dotenv()

API_KEY = (os.getenv("GOOGLE_API_KEY") or "").strip()
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in .env")

MODEL_NAME = (os.getenv("GEMINI_MODEL") or "gemini-2.5-flash").strip()
client = genai.Client(api_key=API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ask_ai(prompt: str) -> str:
    try:
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return (getattr(resp, "text", "") or "").strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {type(e).__name__}: {str(e)}")

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}

def is_definition_question(q: str) -> bool:
    q = q.lower()
    definition_keywords = [
        "what is", "explain", "define", "definition", "meaning of"
    ]
    return any(k in q for k in definition_keywords)


@app.get("/pdf/retirement-overview")
async def get_pdf():
    pdf_path = "../docs/data_sources/Retirement Plan Overview.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found.")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="Retirement Plan Overview.pdf"
    )


@app.post("/api/ai/generate")
async def generate(req: Request):
    data = await req.json()

    user_question = (data.get("question") or "").strip()
    topic_key = data.get("topicKey")
    label = data.get("label")

    if not user_question:
        raise HTTPException(status_code=400, detail="Missing 'question'.")

    cache_key = make_cache_key(user_question, topic_key)
    cached = cache_get(cache_key)
    if cached:
        return {**cached, "cached": True, "label_used": label}

    # ---------------------------------------------------------
    # 1. Retrieve chunks (PDF for definitions, Fidelity for rules)
    # ---------------------------------------------------------
    if is_definition_question(user_question):
        retrieved_chunks = retrieve_definition_chunks(topic_key)
    else:
        retrieved_chunks = retrieve_numeric_chunks(topic_key)

    if not retrieved_chunks:
        raise HTTPException(500, "No chunks retrieved — check chunking pipeline.")

    # ---------------------------------------------------------
    # 2. Build main prompt
    # ---------------------------------------------------------
    single_prompt = f"""
    Answer the question below in Markdown. Keep the explanation short and use simple language.
    Do not include examples.

    Question:
    \"\"\"{user_question}\"\"\"

    After the Markdown answer, on a new line output a JSON object EXACTLY in this format:
    {{"validation":"valid"|"invalid"|"uncertain","confidence":1}}

    - validation must be one of: valid, invalid, uncertain
    - confidence is an integer 1-5
    - Do not output any other JSON or text on the same line as the JSON object.
    """.strip()

    raw = ask_ai(single_prompt)

    # ---------------------------------------------------------
    # 3. Parse JSON token
    # ---------------------------------------------------------
    answer_text, meta = parse_validation_json(raw)

    validated = True
    original_answer = None

    # ---------------------------------------------------------
    # 4. Self-validation repair
    # ---------------------------------------------------------
    if meta["validation"] in ["invalid", "uncertain"]:
        validated = False
        original_answer = answer_text
        repair_prompt = build_repair_prompt(original_answer, user_question)
        repaired_raw = ask_ai(repair_prompt)
        repaired_answer, _ = parse_validation_json(repaired_raw)
        final_answer = repaired_answer
    else:
        final_answer = answer_text

    # ---------------------------------------------------------
    # 5. Add citations
    # ---------------------------------------------------------
    answer_with_citations, citation_map = format_with_citations(
        final_answer,
        retrieved_chunks
    )

    # ---------------------------------------------------------
    # 6. External validator
    # ---------------------------------------------------------
    validation = validate_answer(
        answer_with_citations,
        citation_map,
        retrieved_chunks
    )

    # ---------------------------------------------------------
    # 7. External repair if needed
    # ---------------------------------------------------------
    if not validation["valid"]:
        validated = False
        original_answer = final_answer

        repair_prompt = build_repair_prompt(final_answer, user_question)
        repaired_raw = ask_ai(repair_prompt)
        repaired_answer, _ = parse_validation_json(repaired_raw)

        answer_with_citations, _ = format_with_citations(
            repaired_answer,
            retrieved_chunks
        )

        final_answer = answer_with_citations
    else:
        final_answer = answer_with_citations

    # ---------------------------------------------------------
    # 8. Suggestions
    # ---------------------------------------------------------
    suggestions = generate_suggestions(final_answer, topic_key=topic_key)

    cache_value = {
        "answer": final_answer,
        "validated": validated,
        "confidence": meta["confidence"],
        "suggestions": suggestions,
        "original_answer": original_answer,
    }
    cache_set(cache_key, cache_value)

    return {
        **cache_value,
        "cached": False,
        "label_used": label,
    }

@app.post("/api/scenario")
async def scenario(req: Request):
    data = await req.json()

    try:
        inputs = {
            "age": int(data.get("age", 0)),
            "retirement_age": int(data.get("retirement_age", 0)),
            "annual_income": float(data.get("annual_income", 0)),
            "current_savings": float(data.get("current_savings", 0)),
            "monthly_contribution": float(data.get("monthly_contribution", 0)),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid scenario input: {e}")

    from scenario_engine import compute_projection
    result = compute_projection(**inputs)

    # Retrieve chunks
    retrieved_chunks = retrieve_numeric_chunks("compound_interest")

    # Build prompt
    rules_text = "\n".join(chunk["text"] for chunk in retrieved_chunks)

    explanation_prompt = f"""
        Explain the following retirement projection in simple language.
        Do not compute anything yourself. Use only the numbers provided.

        Projection data:
        {json.dumps(result, indent=2)}

        You must base your explanation only on the financial rules in the section labeled FINANCIAL_RULES.
        Do not use any outside knowledge or assumptions.

        FINANCIAL_RULES:
        {rules_text}
        END_FINANCIAL_RULES

        At all times, restrict your explanation to the FINANCIAL_RULES section.
        If a concept is not present in FINANCIAL_RULES, do not mention it.
        """

    # Ask AI
    raw_explanation = ask_ai(explanation_prompt)

    # Apply citation formatting
    final_explanation, citation_map = format_with_citations(raw_explanation, retrieved_chunks)

    return {
        "explanation": final_explanation,
        "citations": citation_map,
    }