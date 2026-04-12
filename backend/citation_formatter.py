def _resolve_chunk_source(chunk: dict) -> dict:
    """
    Normalise a chunk's source name and URL into a display-ready dict.
    Returns: { name, url, label, is_pdf }
    """
    source = chunk.get("source", "")
    url = chunk.get("url", "")
    section = chunk.get("section", "").replace("_", " ").title()
 
    if "Northwestern" in source:
        return {
            "name": "Northwestern Mutual",
            "url": "http://localhost:8000/pdf/retirement-overview",
            "label": "Retirement Plan Overview (PDF)",
            "is_pdf": True,
        }
 
    if source == "IRS":
        return {
            "name": "IRS",
            "url": url,
            "label": f"IRS.gov — {section}" if section else "IRS.gov",
            "is_pdf": False,
        }
 
    # Fidelity or any future web source — use the actual chunk URL
    # so each topic page (roth_ira, 401k, etc.) gets its own link
    # rather than all collapsing to a single Fidelity URL.
    label = f"{source} — {section}" if section else source
    return {
        "name": source,
        "url": url,
        "label": label,
        "is_pdf": url.lower().endswith(".pdf"),
    }
 
 
def format_with_citations(answer: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return answer, {}, "", answer, ""
 
    # ── Collect all unique sources from every retrieved chunk ──────────────
    seen_urls = set()
    unique_sources = []
 
    for chunk in retrieved_chunks:
        resolved = _resolve_chunk_source(chunk)
        if resolved["url"] not in seen_urls:
            seen_urls.add(resolved["url"])
            unique_sources.append(resolved)
 
    # ── Primary source (first unique) for citation_map ────────────────────
    primary = unique_sources[0]
 
    citation_map = {
        "main": {
            "source": primary["name"],
            "url": primary["url"],
            "type": retrieved_chunks[0].get("type"),
        },
        # All sources keyed by name for multi-source validator lookup
        "all": {s["name"].lower(): s for s in unique_sources},
    }
 
    # ── Inline citation line — lists every contributing source ────────────
    # e.g. "According to [Fidelity](url), [IRS](url), and [Northwestern Mutual](url),"
    linked_names = [f"[{s['name']}]({s['url']})" for s in unique_sources]
 
    if len(linked_names) == 1:
        citation_line = f"According to {linked_names[0]},"
    elif len(linked_names) == 2:
        citation_line = f"According to {linked_names[0]} and {linked_names[1]},"
    else:
        citation_line = (
            "According to "
            + ", ".join(linked_names[:-1])
            + f", and {linked_names[-1]},"
        )
 
    # ── Sources block ─────────────────────────────────────────────────────
    sources_lines = ["---", "**Sources**"]
    for s in unique_sources:
        icon = "📄" if s["is_pdf"] else "🔗"
        sources_lines.append(f"- {icon} [{s['name']} — {s['label']}]({s['url']})")
    sources_block = "\n".join(sources_lines)
 
    # ── Full answer string (for cache / validator) ────────────────────────
    full_answer = f"{citation_line}\n\n{answer.lstrip()}\n\n{sources_block}"
 
    return full_answer, citation_map, citation_line, answer.strip(), sources_block
 