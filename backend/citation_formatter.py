import re

def build_source_phrase(chunk):
    """
    Builds a natural-language citation phrase with a hyperlink.
    Example output:
    "According to [Fidelity](https://www.fidelity.com/retirement-ira/roth-ira)"
    """

    source = chunk["source"]
    section = chunk.get("section", "")
    url = chunk.get("url", None)

    # If URL exists, make the source name clickable
    if url:
        link = f"[{source}]({url})"
    else:
        link = source

    # Natural language phrasing
    if "Fidelity" in source:
        return f"According to {link}"
    elif "Northwestern" in source:
        return f"According to {link}"
    else:
        return f"According to {link}"


def format_with_citations(answer: str, retrieved_chunks: list):
    """
    Instead of [1], [2], this inserts natural-language citations like:
    "According to Fidelity (link)..."
    """

    citation_map = {}
    citation_phrases = []

    # Build citation metadata + natural language phrases
    for i, chunk in enumerate(retrieved_chunks, start=1):
        citation_map[str(i)] = {
            "id": chunk["id"],
            "source": chunk["source"],
            "section": chunk.get("section", ""),
            "url": chunk.get("url", None),
            "text": chunk["text"]
        }

        phrase = build_source_phrase(chunk)
        citation_phrases.append(phrase)

    # Insert citations at the end of the answer
    # Example:
    # "Traditional IRA withdrawals are taxed. According to Fidelity..."
    formatted_answer = answer.strip()

    for phrase in citation_phrases:
        formatted_answer += f" {phrase}."

    return formatted_answer, citation_map