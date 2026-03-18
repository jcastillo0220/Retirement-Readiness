### 1. Strengthen Grounding Checks
- Go beyond source presence:
  - verify that key claims in the answer are actually supported by retrieved chunks
- At minimum:
  - match key phrases (not just numbers)
  - ensure answer content overlaps meaningfully with source text

---

### 2. Improve Citation Validation
- Replace hardcoded logic (e.g., `"Northwestern"`) with a general rule:
  - detect source type dynamically (PDF, web, etc.)
- Validate:
  - cited source exists
  - citation format is consistent
- Use `extract_citation_phrases()` in validation logic (currently unused)

---

### 3. Integrate Repair Loop
- If validation fails:
  - automatically call `build_repair_prompt()`
  - regenerate answer
  - re-run validation
- Limit retries (e.g., 2–3 attempts)
- Return clear failure message if still invalid
