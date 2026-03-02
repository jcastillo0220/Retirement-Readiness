import os
import time
import json
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from google import genai  # ✅ NEW SDK

from generator import generate_suggestions

# ---------------------------------------
# Load env + configure GenAI Client
# ---------------------------------------
load_dotenv()

API_KEY = (os.getenv("GOOGLE_API_KEY") or "").strip()
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in backend/.env (GOOGLE_API_KEY=your_key_here)")

# Pick a model that exists in the NEW API.
# If this one fails, we’ll list models and choose yours.
MODEL_NAME = (os.getenv("GEMINI_MODEL") or "gemini-2.0-flash").strip()

client = genai.Client(api_key=API_KEY)

# ---------------------------------------
# FastAPI app + CORS
# ---------------------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Simple in-memory TTL cache
# ---------------------------
CACHE_TTL = 60 * 60  # 1 hour
CACHE_MAX_ITEMS = 1000
_cache = {}

def _make_cache_key(prompt: str, topic_key: Optional[str]):
    key = (prompt or "").strip().lower()
    if topic_key:
        key = f"{topic_key}||{key}"
    return key

def _cache_get(key: str):
    entry = _cache.get(key)
    if not entry:
        return None
    if time.time() - entry["ts"] > CACHE_TTL:
        del _cache[key]
        return None
    return entry

def _cache_set(key: str, value: dict):
    if len(_cache) >= CACHE_MAX_ITEMS:
        oldest_key = min(_cache.items(), key=lambda kv: kv[1]["ts"])[0]
        del _cache[oldest_key]
    value["ts"] = time.time()
    _cache[key] = value

# ---------------------------
# AI helper functions
# ---------------------------
def ask_ai(prompt: str) -> str:
    if not isinstance(prompt, str) or not prompt.strip():
        return ""
    try:
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        text = getattr(resp, "text", "") or ""
        return text.strip()
    except Exception as e:
        # return a clean error so you can see the true cause in browser too
        raise HTTPException(status_code=500, detail=f"Gemini error: {type(e).__name__}: {str(e)}")

def repair_answer(original_answer: str, original_question: str) -> str:
    repair_prompt = f"""
Your previous answer was flagged as inaccurate or unclear.

Rewrite the explanation correctly.

Rules:
- Use simple language
- Keep it short
- No examples
- Base your explanation ONLY on trusted sources like:
  - https://www.fidelity.com/learning-center/smart-money/retirement-accounts
  - https://www.irs.gov/retirement-plans/plan-sponsor/types-of-retirement-plans
  when applicable
- Stay strictly on topic

Original question:
\"\"\"{original_question}\"\"\"

Original answer:
\"\"\"{original_answer}\"\"\"

Now produce a corrected answer in Markdown.
""".strip()
    return ask_ai(repair_prompt)

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}

# ---------------------------
# Main API endpoint
# ---------------------------
@app.post("/api/ai/generate")
async def generate(req: Request):
    data = await req.json()

    user_question = (data.get("question") or "").strip()
    topic_key = data.get("topicKey")
    label = data.get("label")

    if not user_question:
        raise HTTPException(status_code=400, detail="Missing 'question'.")

    cache_key = _make_cache_key(user_question, topic_key)
    cached = _cache_get(cache_key)
    if cached:
        return {
            "answer": cached["answer"],
            "validated": cached["validated"],
            "confidence": cached.get("confidence", 1),
            "suggestions": cached.get("suggestions", []),
            "original_answer": cached.get("original_answer"),
            "cached": True,
            "label_used": label,
            "label_prompt": cached.get("label_prompt"),
        }

    single_prompt = f"""
Answer the question below in Markdown. Keep the explanation short and use simple language.
Do not include examples.

Question:
\"\"\"{user_question}\"\"\"

After the Markdown answer, on a new line output a JSON object EXACTLY in this format:
{{"validation":"valid"|"invalid"|"uncertain","confidence":1}}

- validation must be one of: valid, invalid, uncertain
- confidence is an integer 1-5 (5 = highest confidence)
- Do not output any other JSON or text on the same line as the JSON object.
""".strip()

    raw = ask_ai(single_prompt)
    label_prompt = ask_ai(label) if isinstance(label, str) and label.strip() else None

    answer_text = raw
    meta = {"validation": "uncertain", "confidence": 1}
    parsed_json = None

    # parse last-line JSON
    try:
        parts = raw.strip().rsplit("\n", 1)
        if len(parts) == 2:
            parsed_json = json.loads(parts[1].strip())
            answer_text = parts[0].strip()
            if isinstance(parsed_json, dict):
                meta["validation"] = parsed_json.get("validation", "uncertain")
                meta["confidence"] = int(parsed_json.get("confidence", 1))
    except Exception:
        parsed_json = None
        meta = {"validation": "uncertain", "confidence": 1}

    validated = True
    original_answer = None

    if meta["validation"] in ["invalid", "uncertain"]:
        original_answer = answer_text
        final_answer = repair_answer(original_answer, user_question)
        validated = False
    else:
        final_answer = answer_text

    suggestions = generate_suggestions(final_answer, topic_key=topic_key)

    cache_value = {
        "answer": final_answer,
        "validated": validated,
        "confidence": meta.get("confidence", 1),
        "suggestions": suggestions,
        "original_answer": original_answer,
        "label_prompt": label_prompt,
    }
    _cache_set(cache_key, cache_value)

    return {
        "answer": final_answer,
        "validated": validated,
        "confidence": meta.get("confidence", 1),
        "suggestions": suggestions,
        "original_answer": original_answer,
        "cached": False,
        "label_used": label,
        "label_prompt": label_prompt,
    }