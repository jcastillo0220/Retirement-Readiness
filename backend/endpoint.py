import os
import logging
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

load_dotenv()

API_KEY = (os.getenv("GOOGLE_API_KEY") or "").strip()
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in .env")

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
    if is_definition_question(user_question):
        retrieved_chunks = retrieve_definition_chunks(topic_key)
    else:
        retrieved_chunks = retrieve_numeric_chunks(topic_key)

    if not retrieved_chunks:
        raise HTTPException(500, "No chunks retrieved.")
        logging.info("Retrieved Chunks:")

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

    raw = ask_ai(single_prompt)

    # ---------------------------
    # 3. REPAIR LOOP ✅
    # ---------------------------
    validated = False
    original_answer = None
    final_answer = ""
    final_confidence = None
    last_errors = []

    current_raw = raw

    for attempt in range(1, MAX_REPAIR_ATTEMPTS + 1):
        logging.info(f"Attempt {attempt}")

        answer_text, meta = parse_validation_json(current_raw)
        final_confidence = meta.get("confidence")

        if original_answer is None:
            original_answer = answer_text

        model_bad = meta.get("validation") in ["invalid", "uncertain"]

        answer_with_citations, citation_map = format_with_citations(
            answer_text,
            retrieved_chunks
        )

        validation = validate_answer(
            answer_with_citations,
            citation_map,
            retrieved_chunks
        )

        if not model_bad and validation["valid"]:
            validated = True
            final_answer = answer_with_citations
            break

        repair_reasons = []

        if model_bad:
            repair_reasons.append("Model flagged answer as invalid/uncertain")

        if not validation["valid"]:
            repair_reasons.extend(validation["errors"])

        last_errors = repair_reasons
        final_answer = answer_with_citations

        if attempt == MAX_REPAIR_ATTEMPTS:
            break

        repair_prompt = build_repair_prompt(
            answer_text,
            user_question,
            repair_reasons
        )

        current_raw = ask_ai(repair_prompt)

    # ---------------------------
    # 4. Suggestions + return
    # ---------------------------
    suggestions = generate_suggestions(final_answer, topic_key=topic_key)
    grounding_report = verify_answer_grounding(final_answer, retrieved_chunks)

    print("CHUNKS:", [c["text"][:200] for c in retrieved_chunks])
    print("GROUNDING REPORT:", grounding_report)

    supported_phrases = [
    g["phrase"] for g in grounding_report if g["supported"]
    ]


    result = {
        "answer": final_answer,
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
        projection, explanation = compute_projection(
            age=data["age"],
            retirement_age=data["retirement_age"],
            annual_income=data["annual_income"],
            current_savings=data["current_savings"],
            monthly_contribution=data["monthly_contribution"],
        )

        return {
            "projection": projection,
            "explanation": explanation,
        }

    except Exception as e:
        raise HTTPException(500, f"Scenario failed: {e}")