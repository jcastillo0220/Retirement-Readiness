def format_with_citations(answer: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return answer, {}

    primary = retrieved_chunks[0]
    source_name = primary["source"]
    source_url = primary["url"]

    is_pdf = False
    if "Northwestern" in source_name:
        source_name = "Northwestern Mutual"
        source_url = "http://localhost:8000/pdf/retirement-overview"
        is_pdf = True

    # 1. Top line
    if is_pdf:
        top_line = f"According to [{source_name}]({source_url}),"
        # Add required blank line for Markdown
        cited_answer = f"{top_line}\n\n{answer.lstrip()}"
    else:
        cited_answer = answer

    # 2. Citation map
    citation_map = {
        "main": {
            "source": source_name,
            "url": source_url
        }
    }

    # 3. Sources section
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

    sources_block = "Sources:\n" + "\n".join(sources_lines)

    # Add blank line before sources block
    cited_answer += f"\n\n{sources_block}"

    return cited_answer, citation_map