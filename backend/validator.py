import json
import re
from extract_citation_phrases import extract_citation_phrases
 
 
def normalize_phrase(phrase: str) -> str:
    p = phrase.lower()
    p = p.replace("according to", "")
    p = p.replace("**", "")
    # Strip all markdown link syntax so we're left with plain source names
    p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)
    return p.strip()
 
 
def find_matching_chunk(normalized_phrase: str, retrieved_chunks: list):
    """Return the first chunk whose source name appears in the normalised phrase."""
    for chunk in retrieved_chunks:
        if chunk["source"].lower() in normalized_phrase:
            return chunk
    return None
 
 
def all_sources_known(normalized_phrase: str, retrieved_chunks: list) -> bool:
    """
    For multi-source citation lines like 'fidelity, irs, and northwestern mutual'
    every source name mentioned must match at least one retrieved chunk.
    Split on common separators and verify each token.
    """
    # Extract individual source tokens from the phrase
    tokens = re.split(r"[,\s]+and\s+|,\s*", normalized_phrase)
    tokens = [t.strip() for t in tokens if t.strip()]
 
    known_sources = {chunk["source"].lower() for chunk in retrieved_chunks}
 
    for token in tokens:
        # Token should match at least one known source (substring match)
        if not any(token in src or src in token for src in known_sources):
            return False
    return True
 
 
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
 
 
def extract_numbers(text: str) -> list:
    """Extract all numeric values (with optional $ prefix and commas) from text."""
    return re.findall(r"\$?\d[\d,]*(?:\.\d+)?", text)
 
 
def normalize_number(num: str) -> str:
    """Strip $ and commas so 7,000 and $7000 both become 7000."""
    return num.replace("$", "").replace(",", "")
 
 
def validate_answer(answer_text: str, citation_map: dict, retrieved_chunks: list):
    errors = []
 
    # 1. Citation format checks
    phrases = extract_citation_phrases(answer_text)
 
    if not phrases:
        return {"valid": False, "errors": ["No citations found"]}
 
    for phrase in phrases:
 
        if not phrase.startswith("According to"):
            errors.append("Citation must start with \'According to\'")
            continue
 
        if "(" not in phrase or ")" not in phrase:
            errors.append("Citation must include a Markdown link")
            continue
 
        normalized = normalize_phrase(phrase)
 
        if not all_sources_known(normalized, retrieved_chunks):
            errors.append("Citation refers to unknown source")
            continue
 
        primary_source = citation_map.get("main", {}).get("source", "").lower()
        if primary_source and primary_source not in normalized:
            errors.append("Citation does not match primary source")
 
    # 2. Numeric cross-check
    answer_nums = {normalize_number(n) for n in extract_numbers(answer_text)}
 
    if answer_nums:
        chunk_nums = set()
        for chunk in retrieved_chunks:
            for n in extract_numbers(chunk.get("text", "")):
                chunk_nums.add(normalize_number(n))
 
        unsupported_nums = answer_nums - chunk_nums
 
        if unsupported_nums and chunk_nums:
            errors.append(
                "Answer contains numbers not found in source chunks: "
                + ", ".join(sorted(unsupported_nums))
            )
 
    if errors:
        return {"valid": False, "errors": errors}
 
    return {"valid": True, "errors": []}