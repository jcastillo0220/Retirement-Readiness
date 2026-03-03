import re

# ---------------------------------------------------------
# Extract all numeric claims from the AI answer
# ---------------------------------------------------------

def extract_numbers(text: str):
    """
    Extracts numbers like:
    - $7,000
    - 59½
    - 10%
    - 12 months
    - 2024
    """
    pattern = r"\$?\d[\d,]*(?:\.\d+)?|\d+½"
    return re.findall(pattern, text)


# ---------------------------------------------------------
# Extract natural-language citation phrases
# ---------------------------------------------------------

def extract_citation_phrases(answer: str):
    """
    Detects phrases like:
    - "According to Fidelity"
    - "According to Northwestern Mutual"
    - "According to Fidelity’s Roth IRA page"
    """
    pattern = r"According to ([A-Za-z0-9 \-\(\)\[\]’]+)"
    return re.findall(pattern, answer)


# ---------------------------------------------------------
# Main validator
# ---------------------------------------------------------

def validate_answer(answer: str, citation_map: dict, retrieved_chunks: list):
    """
    Validates:
    1. Numeric claims appear in retrieved chunks
    2. Citations match the retrieved chunk sources
    3. No unsupported statements
    """

    errors = []

    # -----------------------------------------------------
    # 1. Validate numeric claims
    # -----------------------------------------------------
    numbers = extract_numbers(answer)
    combined_chunk_text = " ".join(chunk["text"] for chunk in retrieved_chunks)

    for num in numbers:
        if num not in combined_chunk_text:
            errors.append(f"Numeric claim '{num}' not found in retrieved sources.")

    # -----------------------------------------------------
    # 2. Validate citation phrases
    # -----------------------------------------------------
    phrases = extract_citation_phrases(answer)

    # Build list of valid sources from retrieved chunks
    valid_sources = set(chunk["source"] for chunk in retrieved_chunks)

    for phrase in phrases:
        # Normalize: "Fidelity’s Roth IRA page" → "Fidelity"
        normalized = phrase.split("’")[0].strip()

        if normalized not in valid_sources:
            errors.append(
                f"Citation phrase 'According to {phrase}' does not match retrieved sources {valid_sources}."
            )

    # -----------------------------------------------------
    # 3. Validate citation_map matches retrieved chunks
    # -----------------------------------------------------
    for key, meta in citation_map.items():
        if meta["source"] not in valid_sources:
            errors.append(
                f"Citation map entry {key} refers to source '{meta['source']}' "
                f"which is not in retrieved sources {valid_sources}."
            )

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }