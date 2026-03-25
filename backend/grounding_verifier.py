import re

def extract_key_phrases(answer: str):
    phrases = re.findall(r"\b([A-Za-z][A-Za-z ]{3,})\b", answer)
    stopwords = {"the","and","or","but","if","a","an","to","of","in","on","for","with"}
    cleaned = [p.strip() for p in phrases if not all(w.lower() in stopwords for w in p.split())]
    return cleaned


def phrase_supported_by_chunks(phrase: str, chunks: list, min_overlap=0.6):
    phrase_words = phrase.lower().split()
    if len(phrase_words) < 2:
        return None

    for chunk in chunks:
        text = chunk["text"].lower()
        overlap = sum(1 for w in phrase_words if w in text) / len(phrase_words)
        if overlap >= min_overlap:
            return {
                "id": chunk.get("id"),
                "text": chunk.get("text")
            }

    return None


def verify_answer_grounding(answer: str, chunks: list):
    phrases = extract_key_phrases(answer)
    report = []

    for phrase in phrases:
        supporting = phrase_supported_by_chunks(phrase, chunks)

        report.append({
            "phrase": phrase,
            "supported": supporting is not None,
            "chunk": supporting  # either {id, text} or None
        })

    return report