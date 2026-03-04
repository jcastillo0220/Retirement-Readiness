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
    Creates ONE clean natural-language citation at the beginning:
    'According to [Fidelity](URL), ...'

    And adds a 'Sources:' section at the bottom.
    """

    if not retrieved_chunks:
        return answer, {}

    # Pick the FIRST chunk as the primary citation
    primary = retrieved_chunks[0]
    source_name = primary["source"]
    source_url = primary["url"]

    # Build clickable Markdown link
    clickable = f"[{source_name}]({source_url})"

    # Insert citation at the beginning
    cited_answer = f"According to {clickable}, {answer.lstrip()}"

    # Build citation map (for validator)
    citation_map = {
        "main": {
            "source": source_name,
            "url": source_url
        }
    }

    # Add sources list at the bottom
    unique_urls = {chunk["url"] for chunk in retrieved_chunks}
    sources_block = "\n\nSources:\n" + "\n".join(f"- {u}" for u in unique_urls)

    cited_answer += sources_block

    return cited_answer, citation_map