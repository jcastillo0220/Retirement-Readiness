def format_with_citations(answer: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return None, answer, "", {}

    # -----------------------------
    # Normalize ALL chunk URLs
    # -----------------------------
    normalized_sources = []
    for chunk in retrieved_chunks:
        name = chunk.get("source")
        url = chunk.get("url")
        source_type = chunk.get("type")

        # Fix PDF URLs globally
        if source_type == "pdf":
            url = "http://localhost:8000/pdf/retirement-overview"

        normalized_sources.append({
            "name": name,
            "url": url,
            "type": source_type,
            "label": chunk.get("section", "").replace("_", " ").title() or name
        })

    # Deduplicate by URL
    unique_sources = []
    seen = set()
    for s in normalized_sources:
        if s["url"] not in seen:
            seen.add(s["url"])
            unique_sources.append(s)

    # Primary source
    primary = unique_sources[0]

    # -----------------------------
    # Build citation line
    # -----------------------------
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

    # -----------------------------
    # Build citation_map
    # -----------------------------
    citation_map = {
        "main": {
            "source": primary["name"],
            "url": primary["url"],
            "type": primary["type"]
        }
    }

    # -----------------------------
    # Build Sources block
    # -----------------------------
    sources_lines = ["---", "**Sources**"]
    for s in unique_sources:
        icon = "📄" if s["type"] == "pdf" else "🔗"
        sources_lines.append(
            f"- {icon} [{s['name']} — {s['label']}]({s['url']})"
        )

    sources_block = "\n".join(sources_lines)

    # -----------------------------
    # Full answer
    # -----------------------------
    full_answer = f"{citation_line}\n\n{answer.strip()}\n\n{sources_block}"

    return full_answer, citation_map, citation_line, answer, sources_block