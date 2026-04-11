# Milestone 2 Grade — Venture 6: Retirement Readiness

**Graded:** April 8, 2026
**Deadline:** April 5, 2026 (end of day)
**Late Commits:** Yes — `MVP_definition.md` was committed April 6 at 11:15 AM (after deadline). Several other commits around midnight 4/5-4/6 are borderline.

---

## Overall Grade: 85/100

---

## Summary

Retirement Readiness has built a substantial system with two working workflows: a definition workflow (RAG pipeline for 5 retirement plan types) and a scenario workflow (deterministic compound interest projections with LLM explanation). The frontend displays citation markers, expandable grounding reports with chunk evidence, and validation status. The codebase shows strong engineering with input sanitization, caching, and a repair loop. However, there are critical bugs (validator phrase-level checks are dead code, scenario endpoint has a tuple unpacking error), a missing required deliverable (`Milestone_2_demo_script.md`), no refusal test cases in evaluation, late submission of `MVP_definition.md`, and a severe contribution imbalance.

### Video Review Notes
The demo video (~6 min) shows both workflows running. **Strengths:** Backend launches showing 33 PDF chunks + 16 Fidelity chunks loaded, clean UI with 5 topic buttons, scenario form produces deterministic projection ($130,284.79), clickable Fidelity citation link verified, and "Validated" badge displayed. **Areas to improve for final demo:** (1) The Roth IRA grounding report shows all 4 phrases as "Not supported" yet the answer is marked "Validated" — the grounding verifier should be connected to the validation decision. (2) Include a proper content-grounding refusal case (out-of-scope question). (3) Demonstrate the repair loop triggering at least once. (4) Show all 5 plan types. (5) Walk through mathematical verification of the projection.

---

## Category Breakdown

### 1. End-to-End Demo Path (22/25)
- Definition workflow: topic selection → retrieval from 3 sources (Northwestern Mutual PDF, Fidelity, IRS) → LLM generation with citations → grounding report. ✓
- Scenario workflow: financial inputs → deterministic compound interest projection → LLM explanation citing Fidelity. ✓
- 5 retirement plan types supported (Roth IRA, 401(k), Traditional IRA, Rollover IRA, Roth 401(k)). ✓
- Citation formatting with "According to [Source](URL)" format. ✓
- Expandable grounding report with Supported/Not Supported per phrase. ✓
- Validation status pill (Validated/Corrected). ✓
- Follow-up suggestion buttons. ✓
- **Critical Bug:** `validator.py` computes `unsupported` phrases and `unsupported_nums` but never adds them to the `errors` list — the function always returns `{"valid": True}`. Phrase-level and numeric grounding checks are effectively dead code.
- **Critical Bug:** `endpoint.py` scenario route attempts tuple unpacking on `verify_answer_grounding()` return, but it returns a list — will crash at runtime.

### 2. Code Quality & Architecture (17/20)
- Clean separation: `chunking.py`, `citation_formatter.py`, `validator.py`, `grounding_verifier.py`, `scenario_engine.py`, `extract_citation_phrases.py`.
- FastAPI with Pydantic models for request validation. ✓
- In-memory cache with 1-hour TTL. ✓
- Input sanitization against prompt injection. ✓
- Multi-turn conversation support. ✓
- `extract_citation_phrases()` is now actively used (Sprint 1 gap addressed). ✓
- **But:** Two critical bugs render key validation features non-functional.
- **Issue:** Many commits are `__pycache__` files (gitignore wasn't set up early enough).

### 3. Documentation & Deliverables (20/25)
- PRD.pdf — 6-page comprehensive document. ✓ (Though PDF format, not .md)
- `evaluation_test_cases.md` — 20 test cases with metrics. ✓
- `risk_log.md` present. ✓
- `spike_results.md` present. ✓
- Architecture diagram present. ✓
- README with setup/run instructions for both backend and frontend. ✓
- `.env.example` present. ✓
- Demo video in zip archive. ✓
- **MISSING:** `Milestone_2_demo_script.md` — a required deliverable.
- **LATE:** `MVP_definition.md` committed April 6 at 11:15 AM — after deadline. Cannot count for full credit.
- **Issue:** No refusal test cases in evaluation (Milestone 2 requires at least 3).
- **Issue:** Scenario test cases 18/19 appear to have swapped generated answers.
- **Issue:** `data_sources/PRD.pdf` is 0 bytes (empty file).

### 4. Evaluation Evidence (13/15)
- 20 test cases documented (17 definition + 3 scenario).
- Honest metrics: 94% retrieval, 100% citation coverage, 48.3% grounding accuracy, 15% hallucination rate.
- Honest acknowledgment of low grounding accuracy is appreciated — but 48.3% and 15% hallucination are concerning.
- **Missing:** Refusal test cases (at least 3 required by spec).

### 5. Repository Hygiene (16/15 — bonus for caching and sanitization)
- `.gitignore` comprehensive. ✓
- `requirements.txt` with correct dependencies. ✓
- `.env.example` present. ✓
- No committed `.env` files. ✓
- Input sanitization and caching are above-and-beyond infrastructure work.

---

## Individual Grades

| Team Member | Commits | Contribution Area | Grade |
|---|---|---|---|
| Joaquin Castillo (jcastillo0220) | 103 | Core AI development — backend, retrieval, validation, scenario engine, grounding verifier | 95/100 |
| Javier Castillo (javi5992) | 77 | Project lead — frontend, UI components, integration, citation formatting | 92/100 |
| Jose Torres | 18 | README, requirements.txt, evaluation test cases, cleanup, repair loop integration | 82/100 |
| Abcde Mireles (asm2-hub) | 4 | PRD upload, merge conflict, refusal mechanism — should increase contributions for final sprint | 65/100 |

**Note:** The Castillo brothers (Joaquin + Javier) led the engineering effort. Abcde Mireles should increase contributions for the final sprint. Jose Torres contributed meaningfully to documentation and evaluation.

---

## Key Recommendations for Sprint 2
1. **Fix the validator bug** — `unsupported` phrases and `unsupported_nums` must be added to the `errors` list and affect the valid/invalid decision.
2. **Fix the scenario endpoint** — `verify_answer_grounding()` returns a list, not a tuple. Fix the unpacking.
3. Write the missing `Milestone_2_demo_script.md`.
4. Add at least 3 refusal test cases to evaluation.
5. Fix swapped scenario test cases (18/19).
6. Address the 48.3% grounding accuracy and 15% hallucination rate — these need significant improvement.
7. Abcde Mireles must take on substantial coding tasks immediately.
8. Convert PRD.pdf to PRD.md for consistency.
