import json
from fastapi import HTTPException

def parse_validation_json(raw: str):
    """
    Extracts the last-line JSON and returns:
    (answer_text, {"validation": str, "confidence": int})
    """
    meta = {"validation": "uncertain", "confidence": 1}

    try:
        parts = raw.strip().rsplit("\n", 1)
        if len(parts) == 2:
            parsed = json.loads(parts[1].strip())
            answer_text = parts[0].strip()

            if isinstance(parsed, dict):
                meta["validation"] = parsed.get("validation", "uncertain")
                meta["confidence"] = int(parsed.get("confidence", 1))

            return answer_text, meta
    except Exception:
        pass

    return raw.strip(), meta


def build_repair_prompt(original_answer: str, original_question: str):
    return f"""
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