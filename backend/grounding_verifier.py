import re
 
 
# ============================================================
# WORD NORMALIZATION
# ============================================================
 
def normalize_words(text: str) -> list:
    """Tokenise text into lowercase alphanumeric words."""
    return re.findall(r"[a-zA-Z0-9]+", (text or "").lower())
 
 
# ============================================================
# ANSWER CLEANING
# Strip citation line, sources block, and markdown formatting
# before phrase extraction so we only check the actual answer
# body — not the auto-generated citation header or sources list.
# ============================================================
 
def clean_answer_for_grounding(answer: str) -> str:
    """
    Remove parts of the answer that are injected by the system
    (citation line, sources block, markdown links) so phrase
    extraction only operates on the substantive answer text.
    """
    lines = (answer or "").splitlines()
    cleaned = []
 
    for line in lines:
        stripped = line.strip()
 
        # Skip citation line
        if stripped.lower().startswith("according to"):
            continue
 
        # Skip sources divider and Sources heading
        if stripped == "---" or stripped.lower().startswith("**sources**"):
            continue
 
        # Skip source bullet lines (- 📄 [...] or - 🔗 [...])
        if re.match(r"^-\s*(📄|🔗|\[)", stripped):
            continue
 
        cleaned.append(line)
 
    # Strip all markdown link syntax [text](url) → text
    text = "\n".join(cleaned)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
 
    # Strip bold/italic markers
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
 
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()
 
 
# ============================================================
# PHRASE EXTRACTION
# ============================================================
 
STOPWORDS = {
    "the", "and", "or", "but", "if", "a", "an", "to", "of", "in", "on",
    "for", "with", "this", "that", "your", "you", "are", "is", "it", "its",
    "be", "as", "at", "by", "from", "was", "were", "has", "have", "had",
    "not", "can", "will", "may", "do", "does", "did", "so", "up", "out",
    "which", "when", "then", "than", "their", "they", "these", "those",
    "also", "more", "some", "any", "all", "both", "each", "into", "through",
    "during", "before", "after", "between", "such", "no", "per", "how",
    "about", "would", "could", "should", "since", "while", "where", "what",
}
 
 
def extract_key_phrases(answer: str) -> list:
    """
    Extract meaningful 3-4 word content phrases from the answer body.
 
    Design decisions to improve grounding accuracy:
    - Clean answer first (remove citation/sources lines)
    - Use 3-4 word sliding window instead of long regex captures
    - Filter phrases that are all stopwords
    - Require at least 2 non-stopword content words per phrase
    - Cap at 15 phrases to avoid checking noise
    """
    cleaned = clean_answer_for_grounding(answer)
 
    # Tokenise into words
    words = re.findall(r"[A-Za-z][a-z]*(?:'[a-z]+)?|\d+(?:\.\d+)?%?|\$\d[\d,]*", cleaned)
    if len(words) < 3:
        return []
 
    phrases = []
    seen = set()
 
    # Sliding window: extract 3-word and 4-word phrases
    for window in (3, 4):
        for i in range(len(words) - window + 1):
            chunk = words[i: i + window]
            phrase = " ".join(chunk)
 
            # Skip if already seen
            if phrase.lower() in seen:
                continue
 
            # Count how many non-stopword, non-trivial words are in the phrase
            content_words = [
                w for w in chunk
                if w.lower() not in STOPWORDS and len(w) > 2
            ]
 
            # Require at least 2 content words in the phrase
            if len(content_words) < 2:
                continue
 
            # Skip phrases that are purely numeric or single-char tokens
            if all(re.match(r"^[\d%$,.]+$", w) for w in chunk):
                continue
 
            seen.add(phrase.lower())
            phrases.append(phrase)
 
    return phrases[:15]
 
 
# ============================================================
# PHRASE SUPPORT CHECK
# ============================================================
 
def phrase_supported(phrase: str, retrieved_chunks: list, min_overlap: float = 0.7) -> bool:
    """
    Check whether a phrase is supported by any retrieved chunk.
 
    Overlap is computed against content words only (stopwords excluded):
        |content_phrase_words ∩ chunk_words| / |content_phrase_words|
 
    Threshold of 0.5: at least half of the phrase's content words
    must appear in a single chunk. Looser than the original 0.75
    because shorter 3-4 word phrases need a proportionally lower bar.
    """
    phrase_words = set(normalize_words(phrase))
    if not phrase_words:
        return False
 
    # Filter stopwords for cleaner overlap scoring
    content_phrase_words = {
        w for w in phrase_words
        if w not in STOPWORDS and len(w) > 2
    }
    if not content_phrase_words:
        return False
 
    for chunk in retrieved_chunks or []:
        chunk_words = set(normalize_words(chunk.get("text", "")))
        if not chunk_words:
            continue
 
        overlap = len(content_phrase_words & chunk_words) / len(content_phrase_words)
        if overlap >= min_overlap:
            return True
 
    return False
 
 
# ============================================================
# GROUNDING REPORT
# ============================================================
 
def verify_answer_grounding(answer: str, retrieved_chunks: list) -> list:
    """
    Extract key phrases from the answer body and check each one
    against the retrieved chunks. Returns a list of dicts:
        [{ "phrase": str, "supported": bool }, ...]
 
    Always returns a list — never raises, never returns None.
    """
    if not answer or not retrieved_chunks:
        return []
 
    phrases = extract_key_phrases(answer)
    if not phrases:
        return []
 
    report = []
    for phrase in phrases:
        supported = phrase_supported(phrase, retrieved_chunks, min_overlap=0.5)
        report.append({
            "phrase": phrase,
            "supported": supported,
        })
 
    return report