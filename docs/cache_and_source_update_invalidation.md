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
- "A 401(k) is a type of employer-sponsored retirement plan. It is considered a qualified plan, alongside others like profit-sharing and money purchase plans. Some 401(k)s may also include a Designated Roth Account option."

#### **401(k) source change**  
Now loads from a different source:  
**Fidelity — What Is a 401(k)?**  
https://www.fidelity.com/learning-center/smart-money/what-is-a-401k

**Answer**
- "A 401(k) is a retirement savings plan that lets you invest a portion of each paycheck before taxes are deducted, depending on the type of contributions made. It is the most popular retirement savings plan, recognized for its tax advantages. Due to these tax advantages, the federal government imposes restrictions on when you can withdraw your contributions."

### Conclusion
After switching the 401(k) source from the Northwestern Mutual PDF to a new web source (Fidelity), the system did not return the same cached answer. Because the chunk loader rebuilt the 401(k) chunks and the backend restarted, the in‑memory cache was cleared and a fresh answer was generated. This confirms that changing the underlying source data results in a new answer, and stale cached responses are not served after a source update.