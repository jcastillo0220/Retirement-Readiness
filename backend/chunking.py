import re
from pathlib import Path
 
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
 
 
TOPIC_MAP = {
    # Definition-like topics
    "definitions": "definitions",
    "roth_ira_definition": "definitions",
    "401k_definition": "definitions",
    "ira_definition": "definitions",
    "rollover_ira_definition": "definitions",
    "roth_401k_definition": "definitions",
 
    # Numeric / rules topics
    "roth_ira": "roth_ira",
    "traditional_ira": "traditional_ira",
    "401k": "401k",
    "rollover_ira": "rollover_ira",
    "roth_401k": "roth_401k",
    "compound_interest": "compound_interest",
}
 
 
BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR.parent / "docs" / "data_sources" / "Retirement Plan Overview.pdf"
 
 
# ============================================================
# 1. GENERIC CHUNKING FUNCTIONS
# ============================================================
 
def chunk_text(text: str, source: str, section: str, url: str, max_words: int = 200):
    words = (text or "").split()
    if not words:
        return []
 
    chunks = []
    current = []
 
    for word in words:
        current.append(word)
        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []
 
    if current:
        chunks.append(" ".join(current))
 
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
# 2. SCRAPING HTML + EXTRACTING TEXT
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
 
 
def scrape_and_chunk_url(url: str, source: str, section: str, max_words: int = 200):
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
 
 
def chunk_pdf(pdf_path: str, source: str, section: str, max_words: int = 200):
    text = extract_text_from_pdf(pdf_path)
    return chunk_text(text, source, section, str(Path(pdf_path).resolve()), max_words=max_words)
 
 
# ============================================================
# 4. SEPARATE CHUNK LISTS
# ============================================================
 
PDF_CHUNKS = []
FIDELITY_CHUNKS = []
IRS_CHUNKS = []
 
 
def load_all_chunks():
    global PDF_CHUNKS, FIDELITY_CHUNKS, IRS_CHUNKS
 
    # Reset first so repeated startup calls don't duplicate data
    PDF_CHUNKS = []
    FIDELITY_CHUNKS = []
    IRS_CHUNKS = []
 
    # -------------------------------
    # LOAD PDF DEFINITIONS
    # (Northwestern Mutual — plain-language definitions)
    # -------------------------------
    try:
        pdf_chunks = chunk_pdf(
            pdf_path=str(PDF_PATH),
            source="Northwestern Mutual",
            section="definitions",
            max_words=200,
        )
        PDF_CHUNKS.extend(pdf_chunks)
        print(f"Loaded {len(pdf_chunks)} PDF definition chunks.")
    except Exception as e:
        print(f"Failed to load PDF: {e}")
 
    # -------------------------------
    # LOAD FIDELITY NUMERIC RULES
    # (Fidelity — practical how-to and contribution rules)
    # -------------------------------
    fidelity_urls = {
        "roth_ira": "https://www.fidelity.com/learning-center/smart-money/what-is-a-roth-ira",
        "traditional_ira": "https://www.fidelity.com/learning-center/smart-money/what-is-an-ira",
        "401k": "https://www.fidelity.com/learning-center/smart-money/what-is-a-401k",
        "rollover_ira": "https://www.fidelity.com/retirement-ira/401k-rollover-ira",
        "roth_401k": "https://www.fidelity.com/learning-center/smart-money/what-is-a-roth-401k",
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
        except Exception as e:
            print(f"Failed to scrape Fidelity URL {url}: {e}")
 
    # -------------------------------
    # LOAD IRS AUTHORITATIVE RULES
    # (IRS.gov — official contribution limits, income thresholds, tax rules)
    # -------------------------------
    irs_urls = {
        "roth_ira": "https://www.irs.gov/retirement-plans/roth-iras",
        "traditional_ira": "https://www.irs.gov/retirement-plans/individual-retirement-arrangements-iras",
        "401k": "https://www.irs.gov/retirement-plans/401k-plans",
        "rollover_ira": "https://www.irs.gov/retirement-plans/plan-participant-employee/rollovers-of-retirement-plan-and-ira-distributions",
        "roth_401k": "https://www.irs.gov/retirement-plans/designated-roth-accounts",
        "compound_interest": "https://www.irs.gov/retirement-plans/retirement-topics-contributions",
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
        except Exception as e:
            print(f"Failed to scrape IRS URL {url}: {e}")
 
 
# ============================================================
# 5. HELPERS
# ============================================================
 
def _with_type(chunk: dict) -> dict:
    copied = dict(chunk)
    url = (copied.get("url") or "").lower()
    copied["type"] = "pdf" if url.endswith(".pdf") else "web"
    return copied
 
 
def _keyword_score(text: str, topic: str) -> int:
    text_l = (text or "").lower()
    topic_words = [w for w in re.findall(r"[a-zA-Z0-9]+", topic.lower()) if len(w) > 2]
    return sum(1 for w in topic_words if w in text_l)
 
 
def _top_scored(chunks: list, topic: str, n: int = 3) -> list:
    """Return up to n chunks from a list, ranked by keyword score."""
    scored = []
    for chunk in chunks:
        score = _keyword_score(chunk.get("text", ""), topic)
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:n]]
 
 
# ============================================================
# 6. RETRIEVAL FUNCTIONS
# ============================================================
 
def retrieve_definition_chunks(topic: str):
    """
    For definition questions: pull from Northwestern Mutual PDF (plain-language
    definitions) AND IRS (authoritative rules), merged together.
    """
    topic = (topic or "definitions").lower()
    section = TOPIC_MAP.get(topic, "definitions")
 
    # Northwestern Mutual — exact section match, fallback to all PDF chunks
    pdf_matches = [
        chunk for chunk in PDF_CHUNKS
        if chunk.get("section", "").lower() == section
    ]
    if not pdf_matches:
        pdf_matches = PDF_CHUNKS
 
    pdf_results = [_with_type(c) for c in pdf_matches[:3]]
 
    # IRS — exact section match, fallback to keyword scoring
    irs_exact = [
        chunk for chunk in IRS_CHUNKS
        if chunk.get("section", "").lower() == section
    ]
    if irs_exact:
        irs_results = [_with_type(c) for c in irs_exact[:2]]
    else:
        irs_results = [_with_type(c) for c in _top_scored(IRS_CHUNKS, topic, n=2)]
 
    return pdf_results + irs_results
 
 
def retrieve_numeric_chunks(topic: str):
    """
    For numeric / rules questions: pull from Fidelity (practical rules) AND
    IRS (official numbers), merged together. Northwestern Mutual PDF is added
    as a fallback if the other two sources are thin.
    """
    topic = (topic or "").lower()
    section = TOPIC_MAP.get(topic)
 
    # ── Fidelity ──────────────────────────────────────────────────────────
    if section:
        fidelity_exact = [
            chunk for chunk in FIDELITY_CHUNKS
            if chunk.get("section", "").lower() == section
        ]
        fidelity_results = [_with_type(c) for c in fidelity_exact[:3]]
    else:
        fidelity_results = [_with_type(c) for c in _top_scored(FIDELITY_CHUNKS, topic, n=3)]
 
    # ── IRS ───────────────────────────────────────────────────────────────
    if section:
        irs_exact = [
            chunk for chunk in IRS_CHUNKS
            if chunk.get("section", "").lower() == section
        ]
        irs_results = [_with_type(c) for c in irs_exact[:2]]
    else:
        irs_results = [_with_type(c) for c in _top_scored(IRS_CHUNKS, topic, n=2)]
 
    merged = fidelity_results + irs_results
 
    # ── Fallback: add Northwestern Mutual PDF if merged is thin ───────────
    if len(merged) < 3:
        pdf_fallback = [_with_type(c) for c in _top_scored(PDF_CHUNKS, topic, n=2)]
        merged += pdf_fallback
 
    # Final safety fallback — never return empty
    if not merged:
        merged = (
            [_with_type(c) for c in FIDELITY_CHUNKS[:3]]
            + [_with_type(c) for c in IRS_CHUNKS[:2]]
        )
 
    return merged