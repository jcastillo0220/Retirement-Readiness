import re
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

TOPIC_MAP = {
    # Definitions (PDF)
    "roth_ira_definition": "definitions",
    "401k_definition": "definitions",
    "ira_definition": "definitions",

    # Numeric rules (Fidelity)
    "roth_ira": "roth_ira",
    "traditional_ira": "traditional_ira",
    "401k": "401k",
    "rollover_ira": "rollover_ira",
    "roth_401k": "roth_401k",
    "compound_interest": "compound_interest",
}

# ============================================================
# 1. GENERIC CHUNKING FUNCTIONS
# ============================================================

def chunk_text(text: str, source: str, section: str, url: str, max_words: int = 200):
    words = text.split()
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
            "text": chunk
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
    return chunk_text(text, source, section, f"file://{pdf_path}", max_words=max_words)


# ============================================================
# 4. SEPARATE CHUNK LISTS
# ============================================================

PDF_CHUNKS = []          # definitions
FIDELITY_CHUNKS = []     # numeric rules


def load_all_chunks():
    global PDF_CHUNKS, FIDELITY_CHUNKS

    # -------------------------------
    # LOAD PDF DEFINITIONS
    # -------------------------------
    try:
        pdf_chunks = chunk_pdf(
            pdf_path="../docs/data_sources/Retirement Plan Overview.pdf",
            source="Northwestern Mutual",
            section="definitions",
            max_words=200
        )
        PDF_CHUNKS += pdf_chunks
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
        "compound_interest": "https://www.fidelity.com/learning-center/trading-investing/compound-interest"
    }

    for section, url in fidelity_urls.items():
        try:
            chunks = scrape_and_chunk_url(
                url=url,
                source="Fidelity",
                section=section,
                max_words=200
            )
            FIDELITY_CHUNKS += chunks
            print(f"Loaded {len(chunks)} Fidelity chunks from {url}")
        except Exception as e:
            print(f"Failed to scrape Fidelity URL {url}: {e}")


# Load chunks at import time
try:
    load_all_chunks()
except Exception as e:
    print(f"Warning: failed to load chunks: {e}")


# ============================================================
# 5. RETRIEVAL FUNCTIONS
# ============================================================

def retrieve_definition_chunks(topic: str):
    topic = topic.lower()

    section = TOPIC_MAP.get(topic, "definitions")

    matches = [
        chunk for chunk in PDF_CHUNKS
        if chunk["section"].lower() == section
    ]

    return matches[:5] if matches else PDF_CHUNKS[:5]

def retrieve_numeric_chunks(topic: str):
    topic = topic.lower()

    section = TOPIC_MAP.get(topic)

    # Exact section match first
    if section:
        exact = [
            chunk for chunk in FIDELITY_CHUNKS
            if chunk["section"].lower() == section
        ]
        if exact:
            return exact[:5]

    # Fallback keyword match
    results = []
    for chunk in FIDELITY_CHUNKS:
        if any(word in chunk["text"].lower() for word in topic.split()):
            results.append(chunk)

    return results[:5] if results else FIDELITY_CHUNKS[:5]