def format_with_citations(answer: str, retrieved_chunks: list):
    """
    Creates ONE clean natural-language citation at the beginning:
    'According to [Source](URL), ...'

    PDF chunks → use backend-served PDF URL
    Fidelity chunks → use real Fidelity URL
    """

    if not retrieved_chunks:
        return answer, {}

    primary = retrieved_chunks[0]
    source_name = primary["source"]
    source_url = primary["url"]

    # -------------------------------
    # 1. Normalize PDF source + URL
    # -------------------------------
    if "Northwestern" in source_name:
        source_name = "Northwestern Mutual"
        source_url = "http://localhost:8000/pdf/retirement-overview"

    # -------------------------------
    # 2. Build clickable link
    # -------------------------------
    clickable = f"[{source_name}]({source_url})"

    cited_answer = f"According to {clickable}, {answer.lstrip()}"

    # -------------------------------
    # 3. Build citation map
    # -------------------------------
    citation_map = {
        "main": {
            "source": source_name,
            "url": source_url
        }
    }

    # -------------------------------
    # 4. Build Sources list
    # -------------------------------
    unique_urls = set()

    for chunk in retrieved_chunks:
        if "Northwestern" in chunk["source"]:
            unique_urls.add("http://localhost:8000/pdf/retirement-overview")
        else:
            unique_urls.add(chunk["url"])

    sources_block = "\n\nSources:\n" + "\n".join(f"- {u}" for u in unique_urls)

    cited_answer += sources_block

    return cited_answer, citation_map