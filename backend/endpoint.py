import os
import re
import logging
from pathlib import Path
from contextlib import asynccontextmanager
 
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from google import genai
 
from generator import generate_suggestions
from cache import make_cache_key, cache_get, cache_set
from validator import parse_validation_json, validate_answer
from scenario_engine import compute_projection
from chunking import (
    load_all_chunks,
    retrieve_definition_chunks,
    retrieve_numeric_chunks,
    IRS_CHUNKS,
)
from citation_formatter import format_with_citations
from grounding_verifier import verify_answer_grounding
 
 
# ============================
# LOGGING
# ============================
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)
 
 
# ============================
# LOAD ENV
# ============================
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
 
API_KEY = (os.getenv("GOOGLE_API_KEY") or "").strip()
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in backend/.env")
 
MODEL_NAME = (os.getenv("GEMINI_MODEL") or "gemini-2.5-flash").strip()
MAX_REPAIR_ATTEMPTS = 3
MAX_Q_LEN = 500
 
# ============================
# FASTAPI LIFESPAN
# ============================
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_all_chunks()
        logger.info("Chunks loaded successfully during startup.")
    except Exception as e:
        logger.warning(f"Chunk load failed: {e}")
    yield
 
 
# ============================
# FASTAPI SETUP
# ============================
app = FastAPI(lifespan=lifespan)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
# ============================
# HELPERS
# ============================
client = genai.Client(api_key=API_KEY)
def ask_ai(prompt: str) -> str:
    try:
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        )
        return (getattr(resp, "text", "") or "").strip()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini error: {type(e).__name__}: {str(e)}"
        )
 
 
def is_definition_question(topic_key: str) -> bool:
    topic_key = (topic_key or "").lower().strip()

    allowed = {
        "roth_ira",
        "traditional_ira",
        "rollover_ira",
    }

    return topic_key in allowed
 
 
def sanitize_question(text: str) -> str:
    text = (text or "").strip()
 
    blocked_patterns = [
        r"(?i)ignore\s+previous\s+instructions",
        r"(?i)ignore\s+all\s+previous\s+instructions",
        r"(?i)system\s+prompt",
        r"(?i)developer\s+message",
        r"(?i)reveal\s+hidden\s+prompt",
        r"(?i)show\s+your\s+chain\s+of\s+thought",
    ]
 
    for pattern in blocked_patterns:
        text = re.sub(pattern, "", text)
 
    text = re.sub(r"\s+", " ", text).strip()
    return text
 
 
def build_source_context(chunks: list) -> str:
    parts = []
    for i, chunk in enumerate(chunks, start=1):
        parts.append(
            f"[Source {i}]\n"
            f"Source Name: {chunk.get('source', 'Unknown')}\n"
            f"Section: {chunk.get('section', 'Unknown')}\n"
            f"URL: {chunk.get('url', '')}\n"
            f"Text: {chunk.get('text', '')}"
        )
    return "\n\n".join(parts)
 
 
def build_repair_prompt(user_question: str, bad_answer: str, repair_reasons: list, source_context: str) -> str:
    issues = "\n".join(f"- {reason}" for reason in repair_reasons) if repair_reasons else "- General failure"
 
    return f"""
Fix the answer below.
 
Question:
{user_question}
 
Bad Answer:
{bad_answer}
 
Issues:
{issues}
 
Use the provided source excerpts if they are helpful. If the sources do not fully support the answer,
you may use general financial knowledge to provide a helpful answer.
Clearly state when any part of the answer is based on general knowledge.
 
Source Excerpts:
{source_context}
 
Rules:
- Keep it simple
- Stay accurate
- Prefer the provided sources when relevant
- No hallucinations
- End with one final JSON line in this exact format:
{{"validation":"valid","confidence":4}}
""".strip()
 
 
def build_fallback_prompt(user_question: str) -> str:
    return f"""
You are a retirement assistant.
 
Answer the question clearly and simply using general financial knowledge.
Be helpful, concise, and use Markdown.
Because this answer is not grounded in the provided project sources, begin with this note:
 
**Note:** This answer is based on general financial knowledge and not the project's loaded sources.
 
Question:
{user_question}
 
After the answer, output one final line of JSON in this exact format:
{{"validation":"valid","confidence":2}}
""".strip()
 
 
# ============================
# ROUTES
# ============================
@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}
 
 
@app.get("/pdf/retirement-overview")
async def get_pdf():
    pdf_path = BASE_DIR.parent / "docs" / "data_sources" / "Retirement Plan Overview.pdf"
 
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF file not found.")
 
    return FileResponse(str(pdf_path), media_type="application/pdf")
 
 
# ============================
# MAIN AI ENDPOINT
# ============================
@app.post("/api/ai/generate")
async def generate(req: Request):
    data = await req.json()
 
    user_question = sanitize_question(data.get("question") or "")
    topic_key = data.get("topicKey") or data.get("topic_key") or "definitions"
    label = data.get("label")
 
    if not user_question:
        raise HTTPException(status_code=400, detail="Missing 'question'.")
 
    if len(user_question) > MAX_Q_LEN:
        raise HTTPException(
            status_code=400,
            detail=f"Question too long (max {MAX_Q_LEN} chars)."
        )
 
    cache_key = make_cache_key(user_question, topic_key)
    cached = cache_get(cache_key)
    if cached:
        return {**cached, "cached": True, "label_used": label}
 
    # ============================
    # 1. RETRIEVE CHUNKS
    # ============================
    print("Retrieving chunks for topic key:", topic_key)
    print("Is definition question?", is_definition_question(user_question))
    print("User question:", user_question)
    if is_definition_question(user_question):
        retrieved_chunks = retrieve_definition_chunks(topic_key)
    else:
        retrieved_chunks = retrieve_numeric_chunks(topic_key)
 
    # ============================
    # 1A. FALLBACK IF NO CHUNKS
    # ============================
    if not retrieved_chunks:
        fallback_raw = ask_ai(build_fallback_prompt(user_question))
        fallback_answer, meta = parse_validation_json(fallback_raw)
 
        result = {
            "answer": fallback_answer,
            "validated": False,
            "confidence": meta.get("confidence", 2),
            "suggestions": generate_suggestions(fallback_answer, topic_key=topic_key),
            "original_answer": None,
            "validation_errors": ["Fallback used: no project sources were retrieved."],
            "supported_phrases": [],
        }
 
        cache_set(cache_key, result)
        return {**result, "cached": False, "label_used": label}
 
    source_context = build_source_context(retrieved_chunks)
 
    # ============================
    # 2. PRIMARY PROMPT
    # ============================
    # Build a deduplicated list of source names actually present in the chunks
    source_names = list(dict.fromkeys(
        c.get("source", "Unknown") for c in retrieved_chunks
    ))
    source_list_str = ", ".join(source_names)
 
    single_prompt = f"""
You are a retirement assistant helping people understand retirement accounts.
 
You have been given excerpts from {len(source_names)} trusted source(s): {source_list_str}.
 
Use ALL of the provided source excerpts to answer the question as accurately as possible.
Where different sources provide complementary information (e.g. Fidelity explains the concept,
IRS confirms the official limit), combine them into a single clear answer.
 
If the sources do not fully support the answer, you may use general financial knowledge,
but clearly state that part is based on general knowledge.
 
Keep the answer short, simple, and in Markdown.
Do NOT include citation lines in your answer — citations are added automatically.
 
Question:
\"\"\"{user_question}\"\"\"
 
Provided Sources:
{source_context}
 
After the answer, output one final line of JSON in this exact format:
{{"validation":"valid","confidence":4}}
""".strip()
 
    current_raw = ask_ai(single_prompt)
 
    # ============================
    # 3. VALIDATION / REPAIR LOOP
    # ============================
    validated = False
    original_answer = None
    final_answer = ""
    final_confidence = None
    last_errors = []
    citation_line = ""
    answer_body = ""
    sources_block = ""
 
    for attempt in range(1, MAX_REPAIR_ATTEMPTS + 1):
        answer_text, meta = parse_validation_json(current_raw)
        final_confidence = meta.get("confidence")
 
        if original_answer is None:
            original_answer = answer_text
 
        model_bad = meta.get("validation") in ["invalid", "uncertain"]
 
        answer_with_citations, citation_map, citation_line, answer_body, sources_block = format_with_citations(
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
            repair_reasons.extend(validation.get("errors", []))
 
        last_errors = repair_reasons
        final_answer = answer_with_citations
 
        if attempt == MAX_REPAIR_ATTEMPTS:
            break
 
        repair_prompt = build_repair_prompt(
            user_question=user_question,
            bad_answer=answer_text,
            repair_reasons=repair_reasons,
            source_context=source_context,
        )
 
        current_raw = ask_ai(repair_prompt)
 
    # ============================
    # 3A. FINAL FALLBACK IF RESULT STILL WEAK
    # ============================
    weak_final = (
        not final_answer.strip()
        or "Not found in provided sources" in final_answer
    )
 
    if weak_final:
        fallback_raw = ask_ai(build_fallback_prompt(user_question))
        fallback_answer, meta = parse_validation_json(fallback_raw)
 
        final_answer = fallback_answer
        final_confidence = meta.get("confidence", 2)
        validated = False
        last_errors = ["Fallback used: retrieved sources were not sufficient for a helpful answer."]
        original_answer = None
 
        result = {
            "answer": final_answer,
            "validated": validated,
            "confidence": final_confidence,
            "suggestions": generate_suggestions(final_answer, topic_key=topic_key),
            "original_answer": original_answer,
            "validation_errors": last_errors,
            "supported_phrases": [],
        }
 
        cache_set(cache_key, result)
        return {**result, "cached": False, "label_used": label}
 
    # ============================
    # 4. POST-VALIDATION / RETURN
    # ============================
    suggestions = generate_suggestions(final_answer, topic_key=topic_key)
    grounding_report = verify_answer_grounding(final_answer, retrieved_chunks)
 
    supported_phrases = [
        g["phrase"] for g in grounding_report if g.get("supported")
    ]
 
    result = {
        "answer": final_answer,
        "citation": citation_line,
        "answer_body": answer_body,
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
 
 
# ============================
# SCENARIO ENDPOINT
# ============================
@app.post("/api/scenario")
async def scenario(req: Request):
    data = await req.json()
 
    try:
        projection, explanation = compute_projection(
            age=int(data["age"]),
            retirement_age=int(data["retirement_age"]),
            annual_income=float(data["annual_income"]),
            current_savings=float(data["current_savings"]),
            monthly_contribution=float(data["monthly_contribution"]),
            return_rate=float(data.get("return_rate", 0.035)),
        )
 
        return {
            "projection": projection,
            "explanation": explanation,
        }
 
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required field: {e.args[0]}"
        )
 
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid scenario input: {str(e)}"
        )
 
    except Exception as e:
        logger.exception("Scenario endpoint failed")
        raise HTTPException(
            status_code=500,
            detail=f"Scenario failed: {str(e)}"
        )