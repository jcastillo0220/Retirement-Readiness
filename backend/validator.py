import json
import re
from extract_citation_phrases import extract_citation_phrases


def normalize_phrase(phrase: str) -> str:
    p = phrase.lower()
    p = p.replace("according to", "")
    p = p.replace("**", "")
    return p.strip()

def find_matching_chunk(normalized_phrase, retrieved_chunks):
    for chunk in retrieved_chunks:
        if chunk["source"].lower() in normalized_phrase:
            return chunk
    return None


def parse_validation_json(raw: str):
    meta = {"validation": "uncertain", "confidence": 1}

    try:
        parts = raw.strip().rsplit("\n", 1)
        if len(parts) == 2:
            parsed = json.loads(parts[1].strip())
            answer_text = parts[0].strip()

            meta["validation"] = parsed.get("validation", "uncertain")
            meta["confidence"] = int(parsed.get("confidence", 1))

            print("Parsed validation JSON successfully:")
            print("Answer text:\n" + answer_text + "\n")
            print("Meta:\n" + str(meta) + "\n")

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


def validate_answer(answer_text, citation_map, retrieved_chunks):
    phrases = extract_citation_phrases(answer_text)

    if not phrases:
        return {"valid": False, "errors": ["No citations found"]}

    for phrase in phrases:

        # 1. Format validation
        if not phrase.startswith("According to"):
            return {"valid": False, "errors": ["Citation must start with 'According to'"]}

        if "(" not in phrase or ")" not in phrase:
            return {"valid": False, "errors": ["Citation must include a Markdown link"]}

        # 2. Normalize
        normalized = normalize_phrase(phrase)

        # 3. Match to retrieved chunks
        chunk = find_matching_chunk(normalized, retrieved_chunks)
        if not chunk:
            return {"valid": False, "errors": ["Citation refers to unknown source"]}

        # 4. Type validation
        if chunk["type"] == "pdf" and not chunk["url"].lower().endswith(".pdf"):
            return {"valid": False, "errors": ["PDF citation mismatch"]}

        if chunk["type"] == "web" and chunk["url"].lower().endswith(".pdf"):
            return {"valid": False, "errors": ["Web citation mismatch"]}

        # 5. Ensure consistency with citation_map
        cited_source = citation_map.get("main", {}).get("source", "").lower()
        if cited_source not in normalized:
            return {"valid": False, "errors": ["Citation does not match primary source"]}

    return {"valid": True, "errors": []}