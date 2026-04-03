def format_with_citations(answer: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return None, answer, "", {}

    primary = retrieved_chunks[0]
    source_name = primary["source"]
    source_url = primary["url"]

    is_pdf = False
    if "Northwestern" in source_name:
        source_name = "Northwestern Mutual"
        source_url = "http://localhost:8000/pdf/retirement-overview"
        is_pdf = True

    # 1. Citation line
    citation_line = None
    if is_pdf:
        citation_line = (
            f"According to "
            f"<a href='{source_url}' class='citation-link'>{source_name}</a>,"
        )

    # 2. Answer body (no top line)
    answer_body = answer.strip()

    # 3. Sources block
    unique_urls = set()
    for chunk in retrieved_chunks:
        if "Northwestern" in chunk["source"]:
            unique_urls.add("http://localhost:8000/pdf/retirement-overview")
        else:
            unique_urls.add(chunk["url"])

    sources_lines = []
    for u in unique_urls:
        if "pdf" in u:
            sources_lines.append(f"- {u} (downloads PDF)")
        else:
            sources_lines.append(f"- {u}")

    sources_block = "Source:\n" + "\n".join(sources_lines)

    citation_map = {
        "main": {
            "source": source_name,
            "url": source_url,
            "type": primary.get("type")
        }
    }

    return citation_line, answer_body, sources_block, citation_map