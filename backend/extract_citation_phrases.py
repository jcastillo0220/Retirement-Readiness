import re

def extract_citation_phrases(answer_text: str):
    """
    Extracts all natural-language citation phrases from the answer.
    Example matches:
      - "According to Fidelity"
      - "According to Northwestern Mutual"
      - "According to [Fidelity](https://...)"
    """

    # Regex explanation:
    # - Look for "According to"
    # - Capture everything until a newline or period
    pattern = r"(According to[^\n\.]+)"

    matches = re.findall(pattern, answer_text)

    # Clean whitespace
    return [m.strip() for m in matches]