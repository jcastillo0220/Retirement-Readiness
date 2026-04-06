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
from validator import parse_validation_json, validate_answer, build_repair_prompt
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
            f"Source Name: {chunk.get('source', 'Unknown')}\n"
            f"Section: {chunk.get('section', 'Unknown')}\n"
            f"URL: {chunk.get('url', '')}\n"
            f"Text: {chunk.get('text', '')}"
        )
    return "\n\n".join(parts)

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
    print("Is definition question?", is_definition_question(topic_key))
    print("User question:", user_question)
    if is_definition_question(topic_key):
        retrieved_chunks = retrieve_definition_chunks(topic_key)
    else:
        retrieved_chunks = retrieve_numeric_chunks(topic_key)
 
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
You are a retirement assistant.
 
Use the provided source excerpts below to answer the question.
Use the provided sources whenever relevant.
Do NOT include any source markers like [source 1], [source 2], or numeric tags.
If the sources do not fully support the answer, you may use general financial knowledge to provide a helpful answer.
 
Keep the answer short, simple, easy to read for beginners, and in Markdown.
A total answer length of 2 - 3 sentences maximum.
 
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
    # 4. POST-VALIDATION / RETURN
    # ============================
    if not validated:
        logging.warning("Answer failed validation after all repair attempts: %s", last_errors)
        return build_refusal_response(
            "Answer could not be grounded after validation: " + "; ".join(last_errors),
            label=label
        )

    suggestions = generate_suggestions(answer_body, topic_key=topic_key)
    grounding_report = verify_answer_grounding(answer_body, retrieved_chunks)
 
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
        # ---------------------------
        # 0. Validate inputs
        # ---------------------------
        required_fields = [
            "age", "retirement_age", "annual_income",
            "current_savings", "monthly_contribution"
        ]

        for f in required_fields:
            if f not in data:
                raise KeyError(f)

        age = int(data["age"])
        retirement_age = int(data["retirement_age"])
        annual_income = float(data["annual_income"])
        current_savings = float(data["current_savings"])
        monthly_contribution = float(data["monthly_contribution"])
        return_rate = float(data.get("return_rate", 0.035))

        if age < 0 or retirement_age < 0 or annual_income < 0 or current_savings < 0 or monthly_contribution < 0:
            raise ValueError("Inputs cannot be negative.")

        if retirement_age < age:
            raise ValueError("Retirement age must be greater than or equal to current age.")

        # ---------------------------
        # 1. Deterministic projection
        # ---------------------------
        projection, raw_explanation = compute_projection(
            age=age,
            retirement_age=retirement_age,
            annual_income=annual_income,
            current_savings=current_savings,
            monthly_contribution=monthly_contribution,
            return_rate=return_rate,
        )

        # ---------------------------
        # 2. Retrieve Fidelity chunks
        # ---------------------------
        retrieved_chunks = retrieve_numeric_chunks("compound_interest")

        # ---------------------------
        # 3. Build clean source context
        # ---------------------------
        source_context = build_source_context(retrieved_chunks)

        # ---------------------------
        # 4. Build LLM prompt
        # ---------------------------
        prompt = f"""
You are a retirement assistant.

Use the provided source excerpts below to explain the scenario.
Use the provided sources whenever relevant.
Do NOT include any source markers like [source 1], [source 2], or numeric tags.
Do NOT invent citations — the system will add them automatically.

Keep the answer short, simple, and easy to read.
Use clear spacing and short sections.
Make the explanation simple, clear, and condensed.

Your output MUST follow this structure:

Explanation of Projection
- Write 2–3 sentences explaining what the projection means.
- You ARE allowed to use the deterministic values provided (age, years to grow, projected balance, return rate).
- Do NOT calculate anything yourself.

Explanation of Inputs
- For each input (age, retirement age, years to grow, income, current savings, monthly contribution, return rate),
  write a short, simple sentence explaining what that input represents.
- Use the provided values, but explain them in your own words.
- Keep each line concise.

Scenario Explanation (context only — do NOT repeat this text directly):
\"\"\"{raw_explanation}\"\"\"

Provided Sources:
{source_context}
"""

        # ---------------------------
        # 5. Ask the LLM
        # ---------------------------
        llm_answer = ask_ai(prompt)

        # ---------------------------
        # 6. Format with citations (5-value return)
        # ---------------------------
        (
            cited_answer,
            citation_map,
            citation_line,
            raw_answer_clean,
            sources_block
        ) = format_with_citations(llm_answer, retrieved_chunks)

        # ---------------------------
        # 7. Validate citations
        # ---------------------------
        validation = validate_answer(
            cited_answer,
            citation_map,
            retrieved_chunks
        )

        # ---------------------------
        # 8. Repair loop if needed
        # ---------------------------
        if not validation["valid"]:
            repair_prompt = build_repair_prompt(
                cited_answer,
                llm_answer,
                validation["errors"]
            )
            repaired = ask_ai(repair_prompt)

            (
                cited_answer,
                citation_map,
                citation_line,
                raw_answer_clean,
                sources_block
            ) = format_with_citations(repaired, retrieved_chunks)

        # ---------------------------
        # 9. Return final response
        # ---------------------------
        return {
            "projection": projection,      # deterministic math
            "explanation": cited_answer,   # LLM explanation with citations
            "citations": citation_map      # Fidelity grounding
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