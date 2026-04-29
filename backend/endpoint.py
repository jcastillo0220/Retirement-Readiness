import os
import re
import logging
import json
import time
import random
from pathlib import Path
from contextlib import asynccontextmanager
 
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError
 
from generator import generate_suggestions
from cache import make_cache_key, cache_get, cache_set
from validator import parse_validation_json, validate_answer, build_repair_prompt, build_repair_prompt_scenario
from scenario_engine import compute_projection
from chunking import (
    load_all_chunks,
    retrieve_definition_chunks,
    retrieve_numeric_chunks,
    is_out_of_scope,
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
 
client = genai.Client(api_key=API_KEY)
 
 
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
def ask_ai(prompt: str, retries=3):
    last_exception = None

    for attempt in range(1, retries + 1):
        try:
            resp = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            return resp.text

        except ServerError as e:
            last_exception = e

            # Retry only on 503 overload
            if e.code == 503:
                sleep = 0.5 * attempt + random.random() * 0.3
                time.sleep(sleep)
                continue

            # Other server errors: stop immediately
            raise HTTPException(
                status_code=500,
                detail=f"Gemini error: {type(e).__name__}: {str(e)}"
            )

    # Retries exhausted
    if last_exception and last_exception.code == 503:
        raise HTTPException(
            status_code=503,
            detail="The AI model is temporarily overloaded. Please try again shortly."
        )

    raise HTTPException(
        status_code=500,
        detail="Unknown Gemini error occurred."
    )
 
 
def is_definition_question(q: str) -> bool:
    if q == "traditional_ira" or q == "roth_ira" or q == "rollover_ira" or q == "401k" or q == "roth_ira_and_roth_401k":
        return True
    else:
        return False
 
 
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
 
def extract_projection_section(answer_text: str) -> str:
    """
    Extract only the 'Explanation of Projection' section for grounding validation.
    """
    lower = answer_text.lower()
    start = lower.find("explanation of projection")
    end = lower.find("explanation of inputs")

    if start == -1:
        return answer_text  # fallback

    if end == -1:
        return answer_text[start:]

    return answer_text[start:end].strip()
 
# ============================
# ANSWER CLEANING
# ============================
def strip_source_links(answer: str) -> str:
    """
    Remove any inline [Source N](url) or [Source N] references that
    Gemini writes when it sees numbered source blocks. These produce
    broken or duplicate links because all Gemini-generated source
    links point to the same chunk URL. Our citation_formatter handles
    all attribution — the answer body should contain no inline links.
    """
    # Remove [Source N](url) markdown links
    pattern_link = r"\[Source\s+\d+\]\([^)]*\)"
    # Remove bare [Source N] references
    pattern_bare = r"\[Source\s+\d+\]"
    answer = re.sub(pattern_link, "", answer)
    answer = re.sub(pattern_bare, "", answer)
    # Clean up any double spaces left behind
    answer = re.sub(r"  +", " ", answer)
    return answer.strip()
 
 
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

    uq = user_question.lower()

    if ("roth ira" in uq and "roth 401" in uq) or ("roth ira" in uq and "roth 401k" in uq):
        topic_key = "roth_ira_and_roth_401k"
 
    if not user_question:
        raise HTTPException(status_code=400, detail="Missing 'question'.")
 
    if len(user_question) > MAX_Q_LEN:
        raise HTTPException(
            status_code=400,
            detail=f"Question too long (max {MAX_Q_LEN} chars)."
        )
 
    # ============================
    # 0. OUT-OF-SCOPE REFUSAL
    # ============================
    if is_out_of_scope(user_question):
        refusal = (
            "This assistant only covers retirement account topics such as IRAs, "
            "401(k) plans, and compound interest. Your question appears to be outside "
            "that scope. Please ask a retirement-related question and I'll be happy to help."
        )
        return {
            "answer": refusal,
            "citation": "",
            "answer_body": refusal,
            "sources": "",
            "validated": False,
            "confidence": 0,
            "suggestions": [],
            "original_answer": None,
            "validation_errors": ["Out-of-scope question — refusal returned."],
            "supported_phrases": [],
            "cached": False,
            "label_used": label,
        }
 
    cache_key = make_cache_key(user_question, topic_key)
    cached = cache_get(cache_key)
    if cached:
        return {**cached, "cached": True, "label_used": label}
 
    # ============================
    # 1. RETRIEVE CHUNKS
    # ============================
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
You are a retirement assistant helping people understand retirement accounts.
 
You have been given excerpts from {len(source_names)} trusted source(s): {source_list_str}.
 
Only Use ALL of the provided source excerpts to answer the question as accurately as possible.
Where different sources provide complementary information (e.g. Fidelity explains the concept,
IRS confirms the official limit), combine them into a single clear answer.
 
Keep the answer short, simple, and in Markdown.
Do NOT include any citation lines, inline source links, or [Source N] references in your answer.
Do NOT write any markdown links at all — no [text](url) syntax anywhere in your answer.
Citations and source links are added automatically after your answer is received.
 
Keep the answer short, simple, easy to read for beginners, and in Markdown.
A total answer length of 3 - 4 sentences.

Question:
\"\"\"{user_question}\"\"\"
 
Provided Sources:
{source_context}
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
 
        # Strip any [Source N](url) inline links Gemini may have written —
        # our citation formatter adds all attribution after this step.
        clean_answer_text = strip_source_links(answer_text)
 
        answer_with_citations, citation_map, citation_line, answer_body, sources_block = format_with_citations(
            clean_answer_text,
            retrieved_chunks
        )
 
        validation = validate_answer(
            answer_body,
            citation_map,
            retrieved_chunks,
            answer_with_citations
        )
        print("Validation result:", validation)
 
        if validation["valid"]:
            validated = True
            final_answer = answer_with_citations
            break
 
        repair_reasons = []
        print("Building repair prompt...")
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

    suggestions = generate_suggestions(final_answer, topic_key=topic_key)
 
    # verify_answer_grounding always returns a list — guard against None
    # in case of unexpected return from older or patched versions.
    raw = verify_answer_grounding(final_answer, retrieved_chunks)

    if isinstance(raw, tuple):
        grounding_report = raw[0] or []
    else:
        grounding_report = raw or []
 
    result = {
        "answer": final_answer,
        "citation": citation_line,
        "answer_body": answer_body,
        "sources": sources_block,
        "validated": validated,
        "is_refusal": False,
        "confidence": final_confidence,
        "suggestions": suggestions,
        "original_answer": original_answer if not validated else None,
        "validation_errors": last_errors if not validated else [],
        "grounding_report": grounding_report,
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
        # ============================
        # 0. Compute numeric projection
        # ============================
        projection, _ = compute_projection(
            age=int(data["age"]),
            retirement_age=int(data["retirement_age"]),
            annual_income=float(data["annual_income"]),
            current_savings=float(data["current_savings"]),
            monthly_contribution=float(data["monthly_contribution"]),
            return_rate=float(data.get("return_rate", 0.035)),
        )

        # ============================
        # 1. Retrieve ONLY compound-interest chunks
        # ============================
        retrieved_chunks = retrieve_numeric_chunks("compound_interest")

        if not retrieved_chunks:
            raise HTTPException(
                status_code=500,
                detail="No compound interest rules available."
            )

        source_context = build_source_context(retrieved_chunks)

        # ============================
        # 2. Build explanation prompt
        # ============================
        single_prompt = f"""
You are a retirement assistant. Explain the following projection using ONLY the provided compound-interest rules.

Projection:
{json.dumps(projection, indent=2)}

Rules:
{source_context}

Your output MUST follow this structure:

Explanation of Projection
- Write 2–3 sentences explaining what the projection means.
- You must used the provided sources and rules.
- Relate it to compound interest growth over time.
- Do NOT calculate anything yourself.

Explanation of Inputs
- Relate the explanation to the specific inputs provided.
- For each input (age, retirement age, years to grow, income, current savings, monthly contribution, return rate [as a percentage], projected balance), 
 write a short, simple sentence explaining what that input represents.
- Keep each line concise.

Do NOT include any markdown links or citations.
After the answer, output one final line of JSON:
Use markdown formatting for the answer.
{{"validation":"valid","confidence":4}}
""".strip()

        current_raw = ask_ai(single_prompt)

        # ============================
        # 3. Validation / Repair Loop
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

            clean_answer_text = strip_source_links(answer_text)

            answer_with_citations, citation_map, citation_line, answer_body, sources_block = (
                format_with_citations(clean_answer_text, retrieved_chunks)
            )

            projection_section = extract_projection_section(answer_body)

            validation = validate_answer(
                projection_section,
                citation_map,
                retrieved_chunks,
                answer_with_citations
            )

            print("Validation result:", validation)
            if validation["valid"]:
                validated = True
                final_answer = answer_with_citations
                break

            repair_reasons = []
            if not validation["valid"]:
                repair_reasons.extend(validation.get("errors", []))

            last_errors = repair_reasons
            final_answer = answer_with_citations

            if attempt == MAX_REPAIR_ATTEMPTS:
                break

            repair_prompt = build_repair_prompt_scenario(
                user_question="Explain this projection.",
                bad_answer=answer_text,
                repair_reasons=repair_reasons,
                source_context=source_context,
            )

            current_raw = ask_ai(repair_prompt)

        # ============================
        # 4. Grounding Report
        # ============================
        raw = verify_answer_grounding(final_answer, retrieved_chunks)
        grounding_report = raw[0] if isinstance(raw, tuple) else raw or []

        # ============================
        # 5. Final Response
        # ============================
        return {
            "projection": projection,
            "answer": final_answer,
            "citation": citation_line,
            "answer_body": answer_body,
            "sources": sources_block,
            "validated": validated,
            "is_refusal": False,
            "confidence": final_confidence,
            "original_answer": original_answer if not validated else None,
            "validation_errors": last_errors if not validated else [],
            "grounding_report": grounding_report,
            "cached": False,
            "label_used": "scenario",
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