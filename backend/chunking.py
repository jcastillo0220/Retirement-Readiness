import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

# ============================================================
# TOPIC MAP
# Maps incoming topic keys to section labels used in chunk metadata.
# Definition keys point to the PDF source.
# Numeric keys point to the Fidelity web source.
# ============================================================

TOPIC_MAP = {
    # Definitions (PDF — Northwestern Mutual)
    "definitions": "definitions",
    "roth_ira_definition": "definitions",
    "401k_definition": "definitions",
    "ira_definition": "definitions",
    "rollover_ira_definition": "definitions",
    "roth_401k_definition": "definitions",

    # Numeric rules (Fidelity web pages)
    "roth_ira": "roth_ira",
    "traditional_ira": "traditional_ira",
    "401k": "401k",
    "rollover_ira": "rollover_ira",
    "roth_401k": "roth_401k",
    "compound_interest": "compound_interest",
}

# ============================================================
# OUT-OF-SCOPE DETECTION
# Queries matching these keywords are flagged as out of scope
# before retrieval is attempted. The endpoint uses this to
# return a refusal response instead of generating an answer.
# ============================================================

OUT_OF_SCOPE_KEYWORDS = [
    # Stock and market speculation
    "stock", "stocks", "ticker", "equity", "equities",
    "buy shares", "sell shares", "market prediction", "market forecast",
    "crypto", "bitcoin", "ethereum", "nft",
    # General personal finance unrelated to retirement accounts
    "mortgage", "home loan", "credit card", "credit score",
    "car loan", "student loan", "debt consolidation",
    # Completely off-topic
    "recipe", "weather", "sports", "movie", "music",
    "restaurant", "travel", "hotel", "flight",
    # Medical / legal (outside scope)
    "doctor", "medication", "lawyer", "lawsuit", "legal advice",
]

RETIREMENT_KEYWORDS = [
    "ira", "401k", "401(k)", "roth", "rollover", "retirement",
    "contribution", "withdrawal", "pension", "savings", "compound interest",
    "traditional ira", "roth ira", "roth 401k", "rollover ira",
]


def is_out_of_scope(question: str) -> bool:
    """
    Returns True if the question contains out-of-scope keywords
    AND does not contain any retirement-related keywords.
    This prevents false positives (e.g. 'stock' appearing in a
    retirement stock allocation question).
    """
    q = (question or "").lower()
    has_oos = any(kw in q for kw in OUT_OF_SCOPE_KEYWORDS)
    has_retirement = any(kw in q for kw in RETIREMENT_KEYWORDS)
    return has_oos and not has_retirement


# ============================================================
# PDF PATH
# Resolved relative to this file so it works regardless of the
# working directory the server is started from.
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR.parent / "docs" / "data_sources" / "Retirement Plan Overview.pdf"


# ============================================================
# 1. GENERIC CHUNKING FUNCTION
# ============================================================

def chunk_text(text: str, source: str, section: str, url: str, max_words: int = 200) -> list:
    """
    Splits text into fixed-size word chunks and returns a list of
    chunk dicts, each with id, source, section, url, and text fields.
    """
    words = (text or "").split()
    if not words:
        return []

    chunks = []
    
    start = 0
    overlap = 50
    
    while start < len(words):
        end = start + max_words
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        
        if chunk_text.strip():
            chunks.append(chunk_text)
        
        start += (max_words - overlap)

    result = []
    for i, chunk in enumerate(chunks, start=1):
        result.append({
            "id": f"{source}_{section}_{i}",
            "source": source,
            "section": section,
            "url": url,
            "text": chunk,
        })

    return result


# ============================================================
# 2. HTML SCRAPING + CHUNKING
# ============================================================

def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.text


def extract_visible_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def scrape_and_chunk_url(url: str, source: str, section: str, max_words: int = 200) -> list:
    html = fetch_html(url)
    text = extract_visible_text_from_html(html)
    return chunk_text(text, source, section, url, max_words=max_words)


# ============================================================
# 3. PDF EXTRACTION + CHUNKING
# ============================================================

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages_text.append(page_text)

    full_text = "\n".join(pages_text)
    full_text = re.sub(r"\s+", " ", full_text)
    return full_text.strip()


def chunk_pdf(pdf_path: str, source: str, section: str, max_words: int = 200) -> list:
    text = extract_text_from_pdf(pdf_path)
    return chunk_text(text, source, section, str(Path(pdf_path).resolve()), max_words=max_words)


# ============================================================
# 4. CHUNK LISTS
# ============================================================

PDF_CHUNKS = []       # Northwestern Mutual — definitions
FIDELITY_CHUNKS = []  # Fidelity — numeric rules
IRS_CHUNKS = []       # IRS - authoritive numeric rules

def load_all_chunks():
    """
    Loads all source chunks into memory at startup.
    Resets lists before loading so repeated calls do not duplicate data.
    Validates chunk counts after each source and logs a warning if a
    source returns fewer than 3 chunks, indicating a scrape or parse failure.
    """
    global PDF_CHUNKS, FIDELITY_CHUNKS, IRS_CHUNKS

    # Reset on every call to prevent duplicates on server reload
    PDF_CHUNKS = []
    FIDELITY_CHUNKS = []
    IRS_CHUNKS = []

    # ── Northwestern Mutual PDF ───────────────────────────────────────────
    if not PDF_PATH.exists():
        print(f"WARNING: PDF not found at {PDF_PATH}. PDF_CHUNKS will be empty.")
    else:
        try:
            pdf_chunks = chunk_pdf(
                pdf_path=str(PDF_PATH),
                source="Northwestern Mutual",
                section="definitions",
                max_words=200,
            )
            PDF_CHUNKS.extend(pdf_chunks)
            print(f"Loaded {len(pdf_chunks)} PDF definition chunks.")

            if len(pdf_chunks) < 3:
                print(f"WARNING: Only {len(pdf_chunks)} PDF chunks loaded — PDF may be malformed or empty.")
        except Exception as e:
            print(f"ERROR: Failed to load PDF: {e}")

    # ── Fidelity web pages ────────────────────────────────────────────────
    fidelity_urls = {
        "roth_ira":          "https://www.fidelity.com/learning-center/smart-money/what-is-a-roth-ira",
        "traditional_ira":   "https://www.fidelity.com/learning-center/smart-money/what-is-an-ira",
        "401k":              "https://www.fidelity.com/learning-center/smart-money/what-is-a-401k",
        "rollover_ira":      "https://www.fidelity.com/retirement-ira/401k-rollover-ira",
        "roth_401k":         "https://www.fidelity.com/learning-center/smart-money/what-is-a-roth-401k",
        "compound_interest": "https://www.fidelity.com/learning-center/trading-investing/compound-interest",
    }

    for section, url in fidelity_urls.items():
        try:
            chunks = scrape_and_chunk_url(
                url=url,
                source="Fidelity",
                section=section,
                max_words=200,
            )
            FIDELITY_CHUNKS.extend(chunks)
            print(f"Loaded {len(chunks)} Fidelity chunks from {url}")

            if len(chunks) < 3:
                print(f"WARNING: Only {len(chunks)} chunks for section '{section}' — page may have blocked the scraper.")
        except Exception as e:
            print(f"ERROR: Failed to scrape Fidelity URL {url}: {e}")
    
    # ── IRS web pages ────────────────────────────────────────────────  
    irs_urls = {
        "roth_ira":        "https://www.irs.gov/retirement-plans/roth-iras",
        "traditional_ira": "https://www.irs.gov/retirement-plans/individual-retirement-arrangements-iras",
        "401k":            "https://www.irs.gov/retirement-plans/401k-plans",
        "rollover_ira":    "https://www.irs.gov/retirement-plans/plan-participant-employee/rollovers-of-retirement-plan-and-ira-distributions",
        "roth_401k":       "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-designated-roth-account",
    }
         
    for section, url in irs_urls.items():
        try:
            chunks = scrape_and_chunk_url(
                url=url,
                source="IRS",
                section=section,
                max_words=200,
            )
            IRS_CHUNKS.extend(chunks)
            print(f"Loaded {len(chunks)} IRS chunks from {url}")

            if len(chunks) < 3:
                print(f"WARNING: Only {len(chunks)} chunks for IRS section '{section}' — page may have blocked the scraper.")
        except Exception as e:
            print(f"ERROR: Failed to scrape IRS URL {url}: {e}")

# ============================================================
# 5. HELPERS
# ============================================================

def _with_type(chunk: dict) -> dict:
    """Adds a 'type' field (pdf or web) to a chunk dict without mutating the original."""
    copied = dict(chunk)
    url = (copied.get("url") or "").lower()
    copied["type"] = "pdf" if url.endswith(".pdf") else "web"
    return copied


def _keyword_score(text: str, topic: str) -> int:
    """Scores a chunk by how many topic words appear in its text."""
    text_l = (text or "").lower()
    topic_words = [w for w in re.findall(r"[a-zA-Z0-9]+", topic.lower()) if len(w) > 2]
    return sum(1 for w in topic_words if w in text_l)


# ============================================================
# 6. RETRIEVAL FUNCTIONS
# ============================================================

def retrieve_definition_chunks(topic: str) -> list:
    """
    Retrieves definition chunks from the Northwestern Mutual PDF.
    Primary: exact section match.
    Fallback: first 5 PDF chunks.
    """
    topic = (topic or "definitions").lower()
    section = TOPIC_MAP.get(topic, "definitions")

    matches = [
        chunk for chunk in PDF_CHUNKS
        if chunk.get("section", "").lower() == section
    ]

    if matches:
        return [_with_type(chunk) for chunk in matches[:5]]

    return [_with_type(chunk) for chunk in PDF_CHUNKS[:5]]


def retrieve_numeric_chunks(topic: str) -> list:
    """
    Retrieves numeric/rules chunks from Fidelity and IRS web pages.
    Primary: exact section match.
    Secondary: keyword-scored fallback across all numeric chunks.
    Final fallback: first 5 numeric chunks.
    """
    topic = (topic or "").lower()
    section = TOPIC_MAP.get(topic)
    
    all_numeric_chunks = FIDELITY_CHUNKS + IRS_CHUNKS

    # 1. Exact section match
    if section:
        exact = [
            chunk for chunk in all_numeric_chunks
            if chunk.get("section", "").lower() == section
        ]
        if exact:
            return [_with_type(chunk) for chunk in exact[:5]]

    # 2. Keyword-scored fallback
    scored = []
    for chunk in all_numeric_chunks:
        score = _keyword_score(chunk.get("text", ""), topic)
        if score > 0:
            scored.append((score, chunk))

    if scored:
        scored.sort(key=lambda x: x[0], reverse=True)
        return [_with_type(chunk) for _, chunk in scored[:5]]

    # 3. Final fallback
    return [_with_type(chunk) for chunk in all_numeric_chunks[:5]]