import json
import re


def parse_validation_json(raw: str):
    meta = {"validation": "uncertain", "confidence": 1}

    try:
        parts = raw.strip().rsplit("\n", 1)
        if len(parts) == 2:
            parsed = json.loads(parts[1].strip())
            answer_text = parts[0].strip()

            meta["validation"] = parsed.get("validation", "uncertain")
            meta["confidence"] = int(parsed.get("confidence", 1))

            return answer_text, meta
    except Exception:
        pass

    return raw.strip(), meta


def build_repair_prompt(answer, question, errors=None):
    error_text = "\n".join(f"- {e}" for e in errors) if errors else "General failure"

    return f"""
Fix the answer below.

Question:
{question}

Bad Answer:
{answer}

Issues:
{error_text}

Rules:
- Keep it simple
- Stay accurate
- Use only provided sources
- No hallucinations

Return:
Answer + JSON validation at end
""".strip()


def extract_numbers(text):
    return re.findall(r"\$?\d[\d,]*(?:\.\d+)?", text)


def normalize(num):
    return num.replace("$", "").replace(",", "")


def validate_answer(answer, citation_map, chunks):
    errors = []

    if not answer:
        return {"valid": False, "errors": ["Empty answer"]}

    combined = " ".join(c.get("text", "") for c in chunks)

    # -----------------
    # Numbers
    # -----------------
    for num in extract_numbers(answer):
        if normalize(num) not in normalize(combined):
            errors.append(f"Number {num} not found in sources")

    # -----------------
    # Citation check
    # -----------------
    if not citation_map or "main" not in citation_map:
        errors.append("Missing citation")

    else:
        source = citation_map["main"].get("source")
        valid_sources = {c.get("source") for c in chunks}

        if source not in valid_sources:
            errors.append("Invalid citation source")

    # -----------------
    # Basic grounding
    # -----------------
    answer_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", answer.lower()))
    source_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", combined.lower()))

    if len(answer_words & source_words) < 3:
        errors.append("Not grounded in source text")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }