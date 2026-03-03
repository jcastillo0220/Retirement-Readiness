import re
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader


# ============================================================
# 1. GENERIC CHUNKING FUNCTIONS
# ============================================================

def chunk_text(text: str, source: str, section: str, url: str, max_words: int = 200):
    """
    Splits long text into ~200-word chunks.
    Returns a list of chunk dicts.
    """
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
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text


def extract_visible_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style
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
# 4. MASTER CHUNK LIST
# ============================================================

CHUNKS = []


def load_all_chunks():
    """
    Add ALL Fidelity URLs here.
    Each URL becomes its own section.
    """

    global CHUNKS

    # -------------------------------
    # FIDELITY RETIREMENT PLAN URLS
    # -------------------------------
    fidelity_urls = {
        "roth_ira": "https://www.fidelity.com/retirement-ira/roth-ira",
        "traditional_ira": "https://www.fidelity.com/retirement-ira/traditional-ira",
        "401k": "https://www.fidelity.com/retirement-ira/401k",
        "rollover_ira": "https://www.fidelity.com/retirement-ira/rollover-ira",
        "roth_401k": "https://www.fidelity.com/retirement-ira/roth-401k"
    }

    for section, url in fidelity_urls.items():
        try:
            CHUNKS += scrape_and_chunk_url(
                url=url,
                source="Fidelity",
                section=section,
                max_words=200
            )
        except Exception as e:
            print(f"Failed to scrape Fidelity URL {url}: {e}")

    # -------------------------------
    # NORTHWESTERN MUTUAL PDF
    # -------------------------------
    try:
        pdf_chunks = chunk_pdf(
            pdf_path="./docs/data_sources/Retirement Plan Overview.pdf",
            source="NorthwesternMutualPDF",
            section="retirement_plans_overview",
            max_words=200
        )
        CHUNKS += pdf_chunks
    except Exception as e:
        print(f"Failed to load PDF: {e}")


# Load chunks at import time
try:
    load_all_chunks()
except Exception as e:
    print(f"Warning: failed to load chunks: {e}")

def retrieve_chunks(question: str):
    # simple keyword-based retrieval
    question_lower = question.lower()
    results = []

    for chunk in CHUNKS:
        if any(word in chunk["text"].lower() for word in question_lower.split()):
            results.append(chunk)

    # fallback: return first 5 chunks
    return results[:5] if results else CHUNKS[:5]