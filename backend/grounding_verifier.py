import re


def normalize_words(text: str):
    return re.findall(r"[a-zA-Z0-9]+", (text or "").lower())


def extract_key_phrases(answer: str):
    phrases = re.findall(r"\b([A-Za-z][A-Za-z ]{6,})\b", answer or "")
    stopwords = {
        "the", "and", "or", "but", "if", "a", "an", "to", "of", "in", "on",
        "for", "with", "this", "that", "your"
    }

    cleaned = []
    for phrase in phrases:
        p = phrase.strip()
        words = p.split()

        if len(words) < 3:
            continue

        if all(w.lower() in stopwords for w in words):
            continue

        if p not in cleaned:
            cleaned.append(p)

    return cleaned[:20]


def phrase_supported(phrase: str, retrieved_chunks: list, min_overlap: float = 0.75):
    phrase_words = set(normalize_words(phrase))
    if not phrase_words:
        return False

    for chunk in retrieved_chunks or []:
        chunk_words = set(normalize_words(chunk.get("text", "")))
        if not chunk_words:
            continue

        overlap = len(phrase_words & chunk_words) / max(len(phrase_words), 1)
        if overlap >= min_overlap:
            return True

    return False


def verify_answer_grounding(answer: str, retrieved_chunks: list):
    phrases = extract_key_phrases(answer)
    report = []

    for phrase in phrases:
      supported = phrase_supported(phrase, retrieved_chunks, min_overlap=0.75)
      report.append({
          "phrase": phrase,
          "supported": supported,
      })

    return report