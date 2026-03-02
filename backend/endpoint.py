import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai

from generator import generate_suggestions
from cache import make_cache_key, cache_get, cache_set
from validation import parse_validation_json, build_repair_prompt

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

    # Build main prompt
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
    label_prompt = ask_ai(label) if isinstance(label, str) and label.strip() else None

    answer_text, meta = parse_validation_json(raw)

    validated = True
    original_answer = None

    if meta["validation"] in ["invalid", "uncertain"]:
        validated = False
        original_answer = answer_text
        repair_prompt = build_repair_prompt(original_answer, user_question)
        final_answer = ask_ai(repair_prompt)
    else:
        final_answer = answer_text

    suggestions = generate_suggestions(final_answer, topic_key=topic_key)

    cache_value = {
        "answer": final_answer,
        "validated": validated,
        "confidence": meta["confidence"],
        "suggestions": suggestions,
        "original_answer": original_answer,
        "label_prompt": label_prompt,
    }
    cache_set(cache_key, cache_value)

    return {
        **cache_value,
        "cached": False,
        "label_used": label,
    }