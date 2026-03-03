import json
import re

# ============================================================
# 1. JSON TOKEN PARSER (your original)
# ============================================================

def parse_validation_json(raw: str):
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


# ============================================================
# 2. REPAIR PROMPT (your original)
# ============================================================

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
- Stay strictly on topic

Original question:
\"\"\"{original_question}\"\"\"

Original answer:
\"\"\"{original_answer}\"\"\"

Now produce a corrected answer in Markdown.
""".strip()


# ============================================================
# 3. EXTERNAL VALIDATOR (numeric + citation + grounding)
# ============================================================

def extract_numbers(text: str):
    pattern = r"\$?\d[\d,]*(?:\.\d+)?|\d+½"
    return re.findall(pattern, text)


def extract_citation_phrases(answer: str):
    pattern = r"According to ([A-Za-z0-9 \-\(\)\[\]’]+)"
    return re.findall(pattern, answer)


def validate_answer(answer: str, citation_map: dict, retrieved_chunks: list):
    errors = []

    # -----------------------------
    # A) Numeric validation
    # -----------------------------
    numbers = extract_numbers(answer)
    combined_chunk_text = " ".join(chunk["text"] for chunk in retrieved_chunks)

    for num in numbers:
        if num not in combined_chunk_text:
            errors.append(f"Numeric claim '{num}' not found in retrieved sources.")

    # -----------------------------
    # B) Citation phrase validation
    # -----------------------------
    phrases = extract_citation_phrases(answer)
    valid_sources = set(chunk["source"] for chunk in retrieved_chunks)

    for phrase in phrases:
        normalized = phrase.split("’")[0].strip()
        if normalized not in valid_sources:
            errors.append(
                f"Citation phrase 'According to {phrase}' does not match retrieved sources {valid_sources}."
            )

    # -----------------------------
    # C) Citation map validation
    # -----------------------------
    for key, meta in citation_map.items():
        if meta["source"] not in valid_sources:
            errors.append(
                f"Citation map entry {key} refers to source '{meta['source']}' "
                f"which is not in retrieved sources {valid_sources}."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }