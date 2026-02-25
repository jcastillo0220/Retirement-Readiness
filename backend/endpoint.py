from fastapi import FastAPI, Request
from google import genai
from fastapi.middleware.cors import CORSMiddleware
import json

from generator import generate_suggestions

API_KEY = "AIzaSyDLXw7TU7ntqZ52NhZ-bNO72qThVNs9I6I"
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
- Base your explanation ONLY on trusted sources like Fidelity or IRS.gov when applicable
- Stay strictly on topic

Original question:
\"\"\"{original_question}\"\"\"

Original answer:
\"\"\"{original_answer}\"\"\"

Now produce a corrected answer in Markdown.
"""
    return ask_ai(repair_prompt)


# ---------------------------
# Main API endpoint (single-call validation)
# ---------------------------

@app.post("/api/ai/generate")
async def generate(req: Request):
    data = await req.json()
    user_question = data["question"]

    # Single prompt: ask for answer, then a JSON validation token on a new line
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

    # Try to split the model output into answer_text and trailing JSON metadata
    answer_text = raw
    meta = {"validation": "uncertain", "confidence": 1}
    parsed_json = None

    # Attempt to extract the last non-empty line as JSON
    try:
        parts = raw.strip().rsplit("\n", 1)
        if len(parts) == 2:
            possible_json = parts[1].strip()
            parsed_json = json.loads(possible_json)
            # If parsed, answer_text is everything before that last line
            answer_text = parts[0].strip()
            # Normalize meta
            if isinstance(parsed_json, dict):
                meta["validation"] = parsed_json.get("validation", "uncertain")
                meta["confidence"] = int(parsed_json.get("confidence", 1))
    except Exception:
        # If parsing fails, keep answer_text as full raw response and meta as uncertain
        parsed_json = None
        meta = {"validation": "uncertain", "confidence": 1}

    # If the model returned the JSON inline (no newline), try to parse trailing JSON substring
    if parsed_json is None:
        # attempt to find a JSON object at the end of the string
        try:
            last_brace = raw.rfind("}")
            first_brace = raw.rfind("{", 0, last_brace + 1)
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                possible_json = raw[first_brace:last_brace + 1]
                parsed_json = json.loads(possible_json)
                # remove the JSON substring from the answer_text
                answer_text = (raw[:first_brace] + raw[last_brace + 1:]).strip()
                if isinstance(parsed_json, dict):
                    meta["validation"] = parsed_json.get("validation", "uncertain")
                    meta["confidence"] = int(parsed_json.get("confidence", 1))
        except Exception:
            parsed_json = None
            meta = {"validation": "uncertain", "confidence": 1}

    # If validation is invalid or uncertain, call repair once (second model call)
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

    # Generate suggestions based on the final answer
    suggestions = generate_suggestions(final_answer)

    return {
        "answer": final_answer,
        "validated": validated,
        "confidence": meta.get("confidence", 1),
        "suggestions": suggestions,
        "original_answer": original_answer,
    }