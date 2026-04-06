import json
import re
from grounding_verifier import extract_key_phrases, extract_numeric_claims, is_financial_number, numeric_claim_supported, phrase_supported
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
 
            print("\nParsed validation JSON successfully:")
            print("Answer text:\n" + answer_text + "\n")
            print("Meta:\n" + str(meta) + "\n")
 
            return answer_text, meta
    except Exception:
        pass
 
    return raw.strip(), meta
 
 
def build_repair_prompt(user_question: str, bad_answer: str, repair_reasons: list, source_context: str) -> str:
    issues = "\n".join(f"- {reason}" for reason in repair_reasons) if repair_reasons else "- General failure"
 
    return f"""
Fix the answer below.
 
Question:
{user_question}
 
Bad Answer:
{bad_answer}
 
Issues:
{issues}
 
Make sure to use only the souces provided below to answer the question. 
Do not include any information that cannot be supported by the provided sources.
 
Do NOT include any source markers like [source 1], [source 2], or numeric tags.
 
Keep the answer short, simple, easy to read for beginners, and in Markdown.
A total answer length of 3 - 4 sentences maximum.

Source Excerpts:
{source_context}
 
Rules:
- Keep it simple
- Stay accurate
- Prefer the provided sources when relevant
- No hallucinations
- End with one final JSON line in this exact format:
{{"validation":"valid","confidence":4}}
""".strip()

def build_repair_prompt_scenario(user_question: str, bad_answer: str, repair_reasons: list, source_context: str) -> str:
    issues = "\n".join(f"- {reason}" for reason in repair_reasons) if repair_reasons else "- General failure"
 
    return f"""
Fix the answer below.
 
Question:
{user_question}
 
Bad Answer:
{bad_answer}
 
Issues:
{issues}
 
You are a retirement assistant.

Use the provided source excerpts below to explain the scenario.
Use the provided sources whenever relevant.
Do NOT include any source markers like [source 1], [source 2], or numeric tags.
Do NOT invent citations — the system will add them automatically.

Keep the answer short, simple, and easy to read.
Use clear spacing and short sections.
Make the explanation simple, clear, and condensed.

Your output MUST follow this structure:

Explanation of Projection
- Write 2–3 sentences explaining what the projection means.
- You ARE allowed to use the deterministic values provided (age, years to grow, projected balance, return rate).
- Do NOT calculate anything yourself.

Explanation of Inputs
- For each input (age, retirement age, years to grow, income, current savings, monthly contribution, return rate),
 write a short, simple sentence explaining what that input represents.
- Keep each line concise.

Source Excerpts:
{source_context}
 
Rules:
- Keep it simple
- Stay accurate
- Prefer the provided sources when relevant
- No hallucinations
- End with one final JSON line in this exact format:
{{"validation":"valid","confidence":4}}
""".strip()
 
 
def extract_numbers(text):
    return re.findall(r"\$?\d[\d,]*(?:\.\d+)?", text)
 
 
def normalize(num):
    return num.replace("$", "").replace(",", "")
 
 
def validate_answer(answer_text: str, citation_map: dict, retrieved_chunks: list):
    errors = []
    phrases = extract_citation_phrases(answer_text)
 
    if not phrases:
        return {"valid": False, "errors": ["No citations found"]}
 
    for phrase in phrases:
 
        # 1. Format validation
        if not phrase.startswith("According to"):
            return {"valid": False, "errors": ["Citation must start with 'According to'"]}
 
        # 2. Normalise — strips markdown links down to plain source names
        normalized = normalize_phrase(phrase)
 
        # 3. Check every source name in the citation is a known retrieved source
        if not all_sources_known(normalized, retrieved_chunks):
            return {"valid": False, "errors": ["Citation refers to unknown source"]}
 
        # 4. Ensure the primary source from citation_map is present
        primary_source = citation_map.get("main", {}).get("source", "").lower()
        if primary_source and primary_source not in normalized:
            return {"valid": False, "errors": ["Citation does not match primary source"]}
 
    # 2. Phrase-level grounding
    phrases = extract_key_phrases(answer_text)

    unsupported = [
        p for p in phrases
        if not phrase_supported(p, retrieved_chunks)
    ]

    # 3. Numeric claim validation
    numeric_claims = [
      n for n in extract_numeric_claims(answer_text)
      if is_financial_number(n)
    ]

    unsupported_nums = [
        n for n in numeric_claims
        if not numeric_claim_supported(n, retrieved_chunks)
    ]

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
