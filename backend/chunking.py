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


def load_all_chunks():
    global PDF_CHUNKS, FIDELITY_CHUNKS

    # Reset first so repeated startup calls don't duplicate data
    PDF_CHUNKS = []
    FIDELITY_CHUNKS = []

    # -------------------------------
    # LOAD PDF DEFINITIONS
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


# ============================================================
# 6. RETRIEVAL FUNCTIONS
# ============================================================

def retrieve_definition_chunks(topic: str):
    topic = (topic or "definitions").lower()
    section = TOPIC_MAP.get(topic, "definitions")

    matches = [
        chunk for chunk in PDF_CHUNKS
        if chunk.get("section", "").lower() == section
    ]

    if matches:
        return [_with_type(chunk) for chunk in matches[:5]]

    fallback = PDF_CHUNKS[:5]
    return [_with_type(chunk) for chunk in fallback]


def retrieve_numeric_chunks(topic: str):
    topic = (topic or "").lower()
    section = TOPIC_MAP.get(topic)

    # 1. Exact section match
    if section:
        exact = [
            chunk for chunk in FIDELITY_CHUNKS
            if chunk.get("section", "").lower() == section
        ]
        if exact:
            return [_with_type(chunk) for chunk in exact[:5]]

    # 2. Keyword-scored fallback
    scored = []
    for chunk in FIDELITY_CHUNKS:
        score = _keyword_score(chunk.get("text", ""), topic)
        if score > 0:
            scored.append((score, chunk))

    if scored:
        scored.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [chunk for _, chunk in scored[:5]]
        return [_with_type(chunk) for chunk in top_chunks]

    # 3. Final fallback
    fallback = FIDELITY_CHUNKS[:5]
    return [_with_type(chunk) for chunk in fallback]