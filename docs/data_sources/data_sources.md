# Structured Data & Source Indexing

---

## Source Registry

| Source | Category | Source Type | URL | Date Collected | MVP Inclusion |
|--------|----------|-------------|-----|----------------|---------------|
| Fidelity — Retirement Accounts | Numeric rules | Consumer financial education web article | https://www.fidelity.com/learning-center/smart-money/retirement-accounts | February 2, 2026 | Yes |
| Fidelity — Roth IRA | Numeric rules | Consumer financial education web article | https://www.fidelity.com/learning-center/smart-money/what-is-a-roth-ira | February 2, 2026 | Yes |
| Fidelity — Traditional IRA | Numeric rules | Consumer financial education web article | https://www.fidelity.com/learning-center/smart-money/what-is-an-ira | February 2, 2026 | Yes |
| Fidelity — 401(k) | Numeric rules | Consumer financial education web article | https://www.fidelity.com/learning-center/smart-money/what-is-a-401k | February 2, 2026 | Yes |
| Fidelity — Rollover IRA | Numeric rules | Consumer financial education web article | https://www.fidelity.com/retirement-ira/401k-rollover-ira | February 2, 2026 | Yes |
| Fidelity — Roth 401(k) | Numeric rules | Consumer financial education web article | https://www.fidelity.com/learning-center/smart-money/what-is-a-roth-401k | February 2, 2026 | Yes |
| Fidelity — Compound Interest | Numeric rules | Consumer financial education web article | https://www.fidelity.com/learning-center/trading-investing/compound-interest | February 2, 2026 | Yes |
| Northwestern Mutual — Retirement Plans Overview | Definitions | Financial institution retirement plan guide (PDF) | Served locally via FastAPI at /pdf/retirement-overview | February 27, 2026 | Yes |
| IRS — Roth IRAs | Authoritative rules | U.S. government regulatory publication | https://www.irs.gov/retirement-plans/roth-iras | April 2026 | Planned |
| IRS — Traditional IRAs | Authoritative rules | U.S. government regulatory publication | https://www.irs.gov/retirement-plans/individual-retirement-arrangements-iras | April 2026 | Planned |
| IRS — 401(k) Plans | Authoritative rules | U.S. government regulatory publication | https://www.irs.gov/retirement-plans/401k-plans | April 2026 | Planned |
| IRS — Rollover Distributions | Authoritative rules | U.S. government regulatory publication | https://www.irs.gov/retirement-plans/plan-participant-employee/rollovers-of-retirement-plan-and-ira-distributions | April 2026 | Planned |
| IRS — Designated Roth Accounts | Authoritative rules | U.S. government regulatory publication | https://www.irs.gov/retirement-plans/designated-roth-accounts | April 2026 | Planned |
| IRS — Retirement Topics: Contributions | Authoritative rules | U.S. government regulatory publication | https://www.irs.gov/retirement-plans/retirement-topics-contributions | April 2026 | Planned |

---

## Source Profiles

### Fidelity

- **Category:** Numeric rules
- **Source type:** Consumer financial education web article
- **Date collected:** February 2, 2026
- **MVP inclusion:** Yes
- **Role in system:** Primary source for numeric rules, contribution limits, withdrawal rules, and growth assumptions
- **How it is used:** Each topic URL is scraped at startup, cleaned from HTML to plain text, and chunked into 200-word segments. Each chunk is labeled with a topic section key (e.g., `compound_interest`, `roth_ira`) and stored in `FIDELITY_CHUNKS`. Retrieved by the numeric retrieval pipeline when the question is not a definition question.

---

### Northwestern Mutual — Retirement Plans Overview (PDF)

- **Category:** Definitions
- **Source type:** Financial institution retirement plan guide (PDF)
- **Date collected:** February 27, 2026
- **MVP inclusion:** Yes
- **Role in system:** Primary source for plain-language definitions of retirement account types
- **How it is used:** The PDF is parsed at startup using PyPDF2, extracted into raw text, and chunked into 200-word segments. All chunks are labeled with section `"definitions"` and stored in `PDF_CHUNKS`. Retrieved by the definition retrieval pipeline when the question contains definition keywords (e.g., "what is", "explain", "define"). The PDF is served locally via a FastAPI route at `/pdf/retirement-overview` so citations can link directly to the document.

---

### IRS (Planned)

- **Category:** Authoritative rules
- **Source type:** U.S. government regulatory publication
- **Date collected:** April 2026 (planned)
- **MVP inclusion:** Planned — not yet active in the MVP build
- **Role in system:** Ground-truth source for official contribution limits, income thresholds, and tax treatment rules. Adds a second authoritative layer alongside Fidelity for numeric questions.
- **How it will be used:** IRS topic pages will be scraped at startup using the same HTML pipeline as Fidelity. Chunks will be stored in a new `IRS_CHUNKS` list and merged with Fidelity results in the numeric retrieval function. Citations will show both sources when both contribute to an answer.

---

## Chunking Strategy

**Overview:**
All source documents are preprocessed into small, self-contained text chunks at startup. This ensures retrieval is precise, citations map cleanly to specific source passages, and grounding validation can be performed reliably.

### PDF Chunking — Northwestern Mutual Definitions

- The PDF is extracted into raw text using PyPDF2.
- Text is cleaned with regex to collapse whitespace.
- Content is segmented into 200-word chunks to maintain semantic coherence.
- Each chunk includes:
  - `id`: unique identifier (e.g., `Northwestern Mutual_definitions_1`)
  - `section`: always `"definitions"` for the PDF source
  - `source`: `"Northwestern Mutual"`
  - `url`: the resolved local file path (used internally); the citation URL is the FastAPI PDF route
  - `text`: the extracted passage

### Web Chunking — Fidelity Numeric Rules

- Each Fidelity URL is fetched and cleaned from HTML to plain text using BeautifulSoup.
- Script, style, and noscript tags are stripped before text extraction.
- Content is segmented into 200-word chunks.
- Each chunk includes:
  - `id`: unique identifier (e.g., `Fidelity_roth_ira_3`)
  - `section`: the topic key (e.g., `compound_interest`, `roth_ira`)
  - `source`: `"Fidelity"`
  - `url`: the original Fidelity page URL
  - `text`: the extracted rule or explanation

### Chunk Count Validation

After loading each source, the system checks that at least 3 chunks were produced. If fewer are returned, a `WARNING` is printed to the server log. This catches silent failures caused by scraper blocks, page structure changes, or PDF parse errors without crashing the server.

### Why This Strategy

- Keeps chunks small enough for accurate grounding verification
- Ensures each chunk maps to a single concept or rule
- Supports topic-aware retrieval with no keyword collisions between topics
- Enables clean citation formatting — each citation can be traced back to a specific chunk
- Makes the system fully auditable: every retrieved chunk is logged with its source, section, and URL

---

## Embedding Strategy

**Overview:** The system uses a controlled, deterministic retrieval approach with no embedding model.

**Rationale:**
- Embeddings introduce nondeterminism, making grounding validation unreliable.
- The system must show exactly which chunk was retrieved and why — this is not possible with vector similarity search.
- Topic-aware section matching achieves the same retrieval precision without the complexity or unpredictability of embeddings.

**Implementation:**
- Retrieval is based on topic keys and section labels assigned during chunking.
- No embedding model is used.
- No similarity vectors are computed.
- No vector database (FAISS, Pinecone, Chroma, etc.) is used.

**Benefits:**
- Fully deterministic — the same question always retrieves the same chunks
- Easy to validate and audit
- Zero risk of retrieving irrelevant content from an unrelated topic

---

## Retrieval Configuration

**Overview:** Retrieval is topic-aware, not similarity-based or keyword-based. The system retrieves chunks using explicit topic-to-section mapping.

| Setting | Value |
|---------|-------|
| Retrieval method | Section-based filtering |
| Similarity metric | None — no embeddings used |
| Top-k | Up to 5 chunks per query |
| Primary rule | Exact section match (e.g., `"compound_interest"` → only compound-interest chunks) |
| Secondary fallback | Keyword-scored match across all chunks in the relevant source list |
| Final fallback | First 5 chunks from the relevant source list (safety net only — should not trigger in normal operation) |

**Why this configuration:**
- Guarantees the correct source is always retrieved for known topics
- Prevents cross-topic contamination (e.g., Roth IRA chunks appearing in compound-interest answers)
- Ensures citations always match retrieved content
- Supports strict grounding validation in the answer pipeline
- The keyword-scored secondary fallback handles free-text questions that do not map to a known topic key
