def format_with_citations(answer: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return None, answer, "", {}

    # Primary source = first retrieved chunk
    primary = retrieved_chunks[0]

    source_name = primary["source"]
    source_url = primary["url"]
    source_type = primary.get("type")  # "pdf" or "web"

    # Detect PDF dynamically
    is_pdf = source_type == "pdf"

    # If it's a PDF, rewrite the URL to your FastAPI PDF endpoint
    if is_pdf:
        source_url = "http://localhost:8000/pdf/retirement-overview"

    # -----------------------------
    # 1. Build citation_line
    # -----------------------------
    if is_pdf:
        citation_line = f"According to [{source_name}]({source_url}),"
    else:
        citation_line = None

    # -----------------------------
    # 2. Build answer_body
    # -----------------------------
    answer_body = answer.strip()

    # -----------------------------
    # 3. Build citation_map
    # -----------------------------
    citation_map = {
        "main": {
            "source": source_name,
            "url": source_url,
            "type": source_type
        }
    }

    # -----------------------------
    # 4. Build Sources section
    # -----------------------------
    unique_urls = set()
    for chunk in retrieved_chunks:
        if chunk["type"] == "pdf":
            unique_urls.add("http://localhost:8000/pdf/retirement-overview")
        else:
            unique_urls.add(chunk["url"])

    sources_lines = []
    for u in unique_urls:
        if u.endswith(".pdf") or "pdf" in u:
            sources_lines.append(f"- {u} (downloads PDF)")
        else:
            sources_lines.append(f"- {u}")

    sources_block = "Source:\n" + "\n".join(sources_lines)

    return citation_line, answer_body, sources_block, citation_map