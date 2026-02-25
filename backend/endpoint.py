import os
import time
import json
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai

from generator import generate_suggestions  # topic-scoped generator

API_KEY = "AIzaSyBxl3MOVTweauPzeeB355Bq0tV2gjUGGnE"
client = genai.Client(api_key=API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

def ask_ai(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

def repair_answer(original_answer: str, original_question: str):
    repair_prompt = f"""
Your previous answer was flagged as inaccurate or unclear.

Rewrite the explanation correctly.

Rules:
- Use simple language
- Keep it short
- No examples
- Base your explanation ONLY on trusted sources like https://www.fidelity.com/learning-center/smart-money/retirement-accounts or https://www.irs.gov/retirement-plans/plan-sponsor/types-of-retirement-plans when applicable
- Stay strictly on topic

Original question:
\"\"\"{original_question}\"\"\"

Original answer:
\"\"\"{original_answer}\"\"\"

Now produce a corrected answer in Markdown.
"""
    return ask_ai(repair_prompt)

# ---------------------------
# Main API endpoint (single-call validation + caching + topic)
# ---------------------------

@app.post("/api/ai/generate")
async def generate(req: Request):
    data = await req.json()
    user_question = data.get("question", "")
    topic_key = data.get("topicKey")  # optional topic key from frontend

    cache_key = _make_cache_key(user_question, topic_key)
    cached = _cache_get(cache_key)
    if cached:
        return {
            "answer": cached["answer"],
            "validated": cached["validated"],
            "confidence": cached.get("confidence", 1),
            "suggestions": cached.get("suggestions", []),
            "original_answer": cached.get("original_answer"),
            "cached": True
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
"""

    raw = ask_ai(single_prompt)

    answer_text = raw
    meta = {"validation": "uncertain", "confidence": 1}
    parsed_json = None

    try:
        parts = raw.strip().rsplit("\n", 1)
        if len(parts) == 2:
            possible_json = parts[1].strip()
            parsed_json = json.loads(possible_json)
            answer_text = parts[0].strip()
            if isinstance(parsed_json, dict):
                meta["validation"] = parsed_json.get("validation", "uncertain")
                meta["confidence"] = int(parsed_json.get("confidence", 1))
    except Exception:
        parsed_json = None
        meta = {"validation": "uncertain", "confidence": 1}

    if parsed_json is None:
        try:
            last_brace = raw.rfind("}")
            first_brace = raw.rfind("{", 0, last_brace + 1)
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                possible_json = raw[first_brace:last_brace + 1]
                parsed_json = json.loads(possible_json)
                answer_text = (raw[:first_brace] + raw[last_brace + 1:]).strip()
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
        repaired = repair_answer(original_answer, user_question)
        final_answer = repaired
        validated = False
    else:
        final_answer = answer_text
        validated = True

    suggestions = generate_suggestions(final_answer, topic_key=topic_key)

    cache_value = {
        "answer": final_answer,
        "validated": validated,
        "confidence": meta.get("confidence", 1),
        "suggestions": suggestions,
        "original_answer": original_answer
    }
    _cache_set(cache_key, cache_value)

    return {
        "answer": final_answer,
        "validated": validated,
        "confidence": meta.get("confidence", 1),
        "suggestions": suggestions,
        "original_answer": original_answer,
        "cached": False
    }