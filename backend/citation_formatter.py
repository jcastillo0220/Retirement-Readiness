def format_with_citations(answer: str, retrieved_chunks: list):
    """
    Rules:
    - Scenario engine (numeric rules): NO 'According to Fidelity' at the top.
    - PDF definitions: KEEP 'According to Northwestern Mutual' at the top.
    - Sources section always appears at the bottom with clickable links.
    - PDF source link must indicate that it downloads a PDF.
    """

    if not retrieved_chunks:
        return answer, {}

    primary = retrieved_chunks[0]
    source_name = primary["source"]
    source_url = primary["url"]

    # Normalize PDF source
    is_pdf = False
    if "Northwestern" in source_name:
        source_name = "Northwestern Mutual"
        source_url = "http://localhost:8000/pdf/retirement-overview"
        is_pdf = True

    # ---------------------------------------------------------
    # 1. Build the TOP LINE (citation phrase)
    # ---------------------------------------------------------

    # If it's a PDF definition → keep "According to ..."
    if is_pdf:
        top_line = f"According to [{source_name}]({source_url}), "
        cited_answer = f"{top_line}{answer.lstrip()}"
    else:
        # Numeric rules (scenario engine) → NO "According to Fidelity"
        cited_answer = answer

    # ---------------------------------------------------------
    # 2. Build citation map
    # ---------------------------------------------------------
    citation_map = {
        "main": {
            "source": source_name,
            "url": source_url
        }
    }

    # ---------------------------------------------------------
    # 3. Build Sources section
    # ---------------------------------------------------------
    unique_urls = set()

    for chunk in retrieved_chunks:
        if "Northwestern" in chunk["source"]:
            unique_urls.add("http://localhost:8000/pdf/retirement-overview")
        else:
            unique_urls.add(chunk["url"])

    # Build formatted sources list
    sources_lines = []
    for u in unique_urls:
        if "pdf" in u:
            sources_lines.append(f"- {u} (downloads PDF)")
        else:
            sources_lines.append(f"- {u}")

    sources_block = "\n\nSources:\n" + "\n".join(sources_lines)

    cited_answer += sources_block

    return cited_answer, citation_map