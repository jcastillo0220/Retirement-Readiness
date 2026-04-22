## Caching Behavior & Source Update Invalidation

### 401(k) Source Update Test (Cache Invalidation Check)
Current Sources Used for 401(k)  
The system currently loads 401(k) from one source:

**Northwestern Mutual — Retirement Plan Overview (PDF)**

This PDF is chunked and stored in memory for retrieval.

### Test Procedure:

**Ask the question:**
- “What is a 401(k)?”

This generates an answer and stores it in the in‑memory cache.

**Answer**
- "A 401(k) is a type of employer-sponsored retirement plan. It is considered a qualified plan. These plans can be structured as pre-tax or as a Designated Roth Account."