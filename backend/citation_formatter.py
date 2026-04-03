def format_with_citations(answer: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return answer, {}, "", answer, ""
 
    primary = retrieved_chunks[0]
    source_name = primary["source"]
    source_url = primary["url"]
 
    if "Northwestern" in source_name:
        source_name = "Northwestern Mutual"
        source_url = "http://localhost:8000/pdf/retirement-overview"
 
    # ── Inline citation line (Markdown hyperlink) ──────────────────────────
    citation_line = f"According to [{source_name}]({source_url}),"
 
    citation_map = {
        "main": {
            "source": source_name,
            "url": source_url,
            "type": primary.get("type"),
        }
    }
 
    # ── Collect all unique sources ─────────────────────────────────────────
    seen = set()
    sources = []
    for chunk in retrieved_chunks:
        if "Northwestern" in chunk["source"]:
            url = "http://localhost:8000/pdf/retirement-overview"
            name = "Northwestern Mutual"
            label = "Retirement Plan Overview (PDF)"
        else:
            url = chunk["url"]
            name = chunk["source"]
            section = chunk.get("section", "").replace("_", " ").title()
            label = section if section else name
 
        if url not in seen:
            seen.add(url)
            is_pdf = "/pdf/" in url or url.lower().endswith(".pdf")
            sources.append({
                "name": name,
                "url": url,
                "label": label,
                "is_pdf": is_pdf,
            })
 
    # ── Build clean Markdown sources block ─────────────────────────────────
    sources_lines = ["---", "**Sources**"]
    for s in sources:
        icon = "📄" if s["is_pdf"] else "🔗"
        sources_lines.append(
            f"- {icon} [{s['name']} — {s['label']}]({s['url']})"
        )
    sources_block = "\n".join(sources_lines)
 
    # ── Full answer string (kept for cache / validator compatibility) ───────
    full_answer = f"{citation_line}\n\n{answer.lstrip()}\n\n{sources_block}"
 
    return full_answer, citation_map, citation_line, answer.strip(), sources_block
 