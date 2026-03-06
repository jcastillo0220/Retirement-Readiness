# Structured Data & Source Indexing

## Fidelity 
***URL: https://www.fidelity.com/learning-center/smart-money/retirement-accounts*** <br>
**Date accessed: February 2, 2026** <br>
*Type of document: Consumer financial education article* <br>
*Role in system: Primary source for numeric rules and information*
- Chunked into 200 word segments
    - Extracted numeric facts, contribution limits, withdrawal rules, and growth assumptions
    - Each chunk labeled with a topic section (e.g., compound_interest)
    - Used by the numeric retrieval pipeline and scenario engine

## Northwestern Mutual – Retirement Plans Overview (PDF)
**Date accessed: February 27, 2026** <br>
*Type of document: Financial institution retirement plan guide* <br>
*Role in system: Primary source for definitions*
- Chunked into 200 word segments
    - Parsed into concept-level definition chunks
    - Only the definitions are extracted
    - Each chunk labeled as "definitions"


## Chunking Strategy
**Overview:**
All source documents (PDF definitions and Fidelity numeric rule pages) are preprocessed into small, self‑contained text chunks. This ensures that retrieval is precise, citations map cleanly to specific source passages, and grounding validation can be performed reliably. <br>

**PDF Chunking (Northwestern Mutual Definitions)**
- The PDF is extracted into raw text using a PDF parser.
- Text is segmented by concept headings (e.g., “Roth IRA”, “401(k)”, “Traditional IRA”).
- Content is segmented into 200 word chunks 
- Each concept becomes a chunk with:
    - section: the concept name
    - source: “Northwestern Mutual”
    - url: the local FastAPI PDF route
    - text: the extracted definition
    - Tables are chunked row‑by‑row to preserve semantic meaning.

**Fidelity Webpage Chunking (Numeric Rules)**
- Each Fidelity URL is fetched and cleaned (HTML → plain text).
- Content is segmented into 200 word chunks to maintain semantic coherence.
- Each chunk includes:
    - section: the topic key (e.g., compound_interest, roth_ira)
    - source: the Fidelity page name
    - url: the original Fidelity URL
    - text: the extracted rule or explanation

**Why this strategy**
- Keeps chunks small enough for accurate grounding
- Ensures each chunk maps to a single concept
- Supports **topic‑aware** retrieval (no keyword collisions)
- Enables clean citation formatting and validation

## Embedding strategy
**Overview:**
Uses a controlled and deterministic retrieval system. <br>

**Rationale**
- Embeddings introduce nondeterminism and make grounding validation harder.
- The system must show exactly which chunk was retrieved and why.
- Topic‑aware retrieval ensures correctness without embeddings.

**Implementation**
- Retrieval is based on:
- Topic keys (e.g., "compound_interest", "roth_ira")
- Section labels assigned during chunking
- No embedding model is used.
- No similarity vectors are computed.
- No vector database (FAISS, Pinecone, Chroma, etc.) is used.

**Benefits**
- Fully deterministic retrieval
- Easy to validate and audit
- Zero risk of retrieving irrelevant content


## Retrieval configuration
**Overview:**
Retrieval is topic‑aware, not similarity‑based or key-word based. The system retrieves chunks using explicit topic to section mapping. <br>

**Configuration**
- **Retrieval method:** Section‑based filtering
- **Similarity metric:** None (no embeddings used)

- **Top‑k:**
    - Up to 5 chunks per query
    - Ensures enough context for grounding without overwhelming the model

- **Primary selection rule:**
    - Exact section match (e.g., "compound_interest" → only compound‑interest chunks)

- **Fallback rule:**
    - Keyword match only if no section match exists
    - **Final fallback:** first 5 chunks (never used in normal operation)

**Why this configuration**
- Guarantees the correct source is always retrieved
- Prevents cross‑topic contamination (e.g., Roth IRA chunks appearing in compound‑interest answers)
- Ensures citations always match retrieved content
- Supports strict grounding validation
