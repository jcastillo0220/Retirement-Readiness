import os
import logging
import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from google import genai

from generator import generate_suggestions
from cache import make_cache_key, cache_get, cache_set
from validator import parse_validation_json, build_repair_prompt, validate_answer
from scenario_engine import compute_projection

from chunking import retrieve_definition_chunks, retrieve_numeric_chunks
from citation_formatter import format_with_citations
from grounding_verifier import verify_answer_grounding

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

API_KEY = input("Enter your Google API key: ").strip()
if not API_KEY:
    raise RuntimeError("You must enter an API key.")

MODEL_NAME = (os.getenv("GEMINI_MODEL") or "gemini-2.5-flash").strip()
MAX_REPAIR_ATTEMPTS = 3

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
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        )
        return (getattr(resp, "text", "") or "").strip()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini error: {type(e).__name__}: {str(e)}"
        )

def strip_after_json_fence(text: str) -> str:
    # Remove anything starting from ```json (or ``` JSON, case‑insensitive)
    return re.split(r"```json", text, flags=re.IGNORECASE)[0].strip()

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}

def is_definition_question(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in ["what is", "define", "explain", "meaning"])

@app.get("/pdf/retirement-overview")
async def get_pdf():
    pdf_path = "../docs/data_sources/Retirement Plan Overview.pdf"

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found.")

    return FileResponse(pdf_path, media_type="application/pdf")

def build_refusal_response(reason: str, label=None):
    return {
        "answer": (
            "I could not find a verified source for that question, "
            "so I can’t provide a grounded answer right now."
        ),
        "validated": False,
        "confidence": 0,
        "suggestions": [],
        "original_answer": None,
        "validation_errors": [reason],
        "supported_phrases": [],
        "cached": False,
        "label_used": label,
        "refused": True,
    }

@app.post("/api/ai/generate")
async def generate(req: Request):
    data = await req.json()

    user_question = (data.get("question") or "").strip()
    topic_key = data.get("topicKey") or data.get("topic_key") or "definitions"
    label = data.get("label")

    if not user_question:
        raise HTTPException(status_code=400, detail="Missing 'question'.")

    cache_key = make_cache_key(user_question, topic_key)
    cached = cache_get(cache_key)
    if cached:
        return {**cached, "cached": True, "label_used": label}

    # ---------------------------
    # 1. Retrieve chunks
    # ---------------------------
    print("==================================================")
    print(f"User question: {user_question}")
    print(is_definition_question(user_question) + "\n\n")
    if is_definition_question(user_question):
        retrieved_chunks = retrieve_definition_chunks(topic_key)
    else:
        retrieved_chunks = retrieve_numeric_chunks(topic_key)

    if not retrieved_chunks:
        logging.warning("No chunks retrieved for question: %s", user_question)
        return build_refusal_response("No verified source retrieved", label=label)

    for i, chunk in enumerate(retrieved_chunks, start=1):
        logging.info(
            f"\n--- Chunk {i} ---\n"
            f"ID: {chunk.get('id')}\n"
            f"url: {chunk.get('url')}\n"
            f"Text:\n{chunk.get('text')}\n"
        )

    # ---------------------------
    # 2. Build prompt
    # ---------------------------
    single_prompt = f"""
    Answer the question below in Markdown. Keep it short and simple.

    Question:
    \"\"\"{user_question}\"\"\"

    After the answer, output:
    {{"validation":"valid","confidence":4}}
    """.strip()

    raw_answer = ask_ai(single_prompt)

    # ---------------------------
    # 3. REPAIR LOOP ✅
    # ---------------------------
    validated = False
    original_answer = None
    final_answer = ""
    final_confidence = None
    last_errors = []

    for attempt in range(1, MAX_REPAIR_ATTEMPTS):
        logging.info(f"Attempt {attempt}")

        answer_text, meta = parse_validation_json(raw_answer)
        final_confidence = meta.get("confidence")

        model_bad = meta.get("validation") in ["invalid", "uncertain"]

        citation_line, answer_body, sources_block, citation_map = format_with_citations(
            answer_text,
            retrieved_chunks
        )

        # For validation, you still need the combined string:
        answer_with_citations = ""

        if citation_line:
            answer_with_citations += citation_line + "\n\n"

        answer_with_citations += answer_body + "\n\n" + sources_block

        validation = validate_answer(
            answer_with_citations,
            citation_map,
            retrieved_chunks
        )

        logging.info(f"Model_bad {model_bad}")
        logging.info(f"Validation: {validation}")
        if not model_bad and validation["valid"]:
            validated = True
            final_answer = answer_with_citations
            break
        else:
            repair_reasons = []

            if model_bad:
                repair_reasons.append("Model flagged answer as invalid/uncertain")

            if not validation["valid"]:
                repair_reasons.extend(validation["errors"])

            last_errors = repair_reasons
            final_answer = answer_with_citations

            repair_prompt = build_repair_prompt(
                answer_text,
                user_question,
                repair_reasons
            )

        if attempt == MAX_REPAIR_ATTEMPTS:
            break

        repair_prompt = build_repair_prompt(
            answer_text,
            user_question,
            repair_reasons
        )

        current_raw = ask_ai(repair_prompt)
        
        if not validated:
            logging.warning("Answer failed validation after all repair attempts: %s", last_errors)
            return build_refusal_response(
                "Answer could not be grounded after validation: " + "; ".join(last_errors),
                label=label
  )
    

    # ---------------------------
    # 4. Suggestions + return
    # ---------------------------
    answer_body = strip_after_json_fence(answer_body)
    suggestions = generate_suggestions(final_answer, topic_key=topic_key)
    grounding_report = verify_answer_grounding(answer_body, retrieved_chunks)

    supported_phrases = [
        {
            "phrase": g["phrase"],
            "chunk_id": g["chunk"]["id"],
            "chunk_text": g["chunk"]["text"]
        }
        for g in grounding_report
        if g["supported"] and g["chunk"] is not None
    ]

    result = {
        "citation": citation_line,
        "answer": answer_body,
        "sources": sources_block,
        "validated": validated,
        "confidence": final_confidence,
        "suggestions": suggestions,
        "original_answer": original_answer if not validated else None,
        "validation_errors": last_errors if not validated else [],
        "supported_phrases": supported_phrases,
    }

    cache_set(cache_key, result)

    return {**result, "cached": False, "label_used": label}

@app.post("/api/scenario")
async def scenario(req: Request):
    data = await req.json()

    try:
        explanation = compute_projection(
            age=data["age"],
            retirement_age=data["retirement_age"],
            annual_income=data["annual_income"],
            current_savings=data["current_savings"],
            monthly_contribution=data["monthly_contribution"],
        )

        return {
            "explanation": explanation,
        }

    except Exception as e:
        raise HTTPException(500, f"Scenario failed: {e}")