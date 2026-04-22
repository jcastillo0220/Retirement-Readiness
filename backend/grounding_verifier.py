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
 
def split_into_clauses(text: str) -> list:
    """
    Split text into natural clauses using punctuation and conjunctions.
    """
    # Break on punctuation
    parts = re.split(r"[.;:!?]", text)

    clauses = []
    for part in parts:
        # Further split on common clause joiners
        subparts = re.split(r"\b(and|but|so|because|while|when|which|that)\b", part)
        for s in subparts:
            cleaned = s.strip()
            if len(cleaned.split()) >= 3:
                clauses.append(cleaned)

    return clauses

def extract_noun_phrases(text: str) -> list:
    """
    Extract simple noun phrases using regex patterns.
    """
    pattern = r"\b(?:[A-Za-z']+\s){0,3}(?:money|taxes|withdrawals|retirement|income|contributions)\b"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return [m.strip() for m in matches]

def extract_verb_phrases(text: str) -> list:
    """
    Extract simple verb-object patterns.
    """
    pattern = r"\b(contribute|withdraw|pay|paid|earn|grow|receive)\s+[A-Za-z']+(?:\s+[A-Za-z']+){0,2}"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return [m.strip() for m in matches]
 
def extract_key_phrases(answer: str) -> list:
    text = clean_answer_for_grounding(answer)
    if not text:
        return []

    clauses = split_into_clauses(text)
    phrases = []
    seen = set()

    for clause in clauses:
        # Noun phrases
        for np in extract_noun_phrases(clause):
            low = np.lower()
            if low not in seen:
                seen.add(low)
                phrases.append(np)

        # Verb phrases
        for vp in extract_verb_phrases(clause):
            low = vp.lower()
            if low not in seen:
                seen.add(low)
                phrases.append(vp)

    return phrases[:15]
 
 
# ============================================================
# PHRASE SUPPORT CHECK
# ============================================================
 
def phrase_supported(phrase: str, retrieved_chunks: list, min_overlap: float = 0.7) -> bool:
    """
    Check whether a phrase is supported by any retrieved chunk.
 
    Overlap is computed against content words only (stopwords excluded):
        |content_phrase_words ∩ chunk_words| / |content_phrase_words|
 
    Threshold of 0.7: at least half of the phrase's content words
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
 
def verify_answer_grounding(answer: str, retrieved_chunks: list):
    print("Verifying answer grounding...")
    phrases = extract_key_phrases(answer)
    report = []

    for phrase in phrases:
        supporting_chunks = []

        for chunk in retrieved_chunks:
            if phrase_supported(phrase, [chunk], min_overlap=0.75):
                supporting_chunks.append({
                    "id": chunk.get("id"),
                    "source": chunk.get("source"),
                    "section": chunk.get("section"),
                    "text": chunk.get("text"),
                })

        report.append({
            "phrase": phrase,
            "supported": len(supporting_chunks) > 0,
            "chunks": supporting_chunks if supporting_chunks else []
        })

    return {
        "supported_phrases": [item for item in report if item["supported"]],
        "unsupported_phrases": [item for item in report if not item["supported"]],
        "full_report": report
    }