# Milestone 2 Deliverables
## Team: Retirement Readiness
### Due: April 5, 2026
### Focus: MVP of a Grounded, Personalized Retirement Planning Assistant

---

## Context

Milestone 1 established the engineering foundation: a RAG pipeline with topic-aware retrieval, citation formatting, a validation and repair loop, a grounding verifier, and a deterministic scenario engine for compound growth projections.

Sprint 1 asked the team to strengthen grounding checks beyond source presence, improve citation validation by removing hardcoded logic, and integrate the repair loop. Milestone 2 is where that work must become concrete. This checkpoint is the MVP review.

Milestone 2 is not about adding broad new scope. It is about demonstrating one narrow, stable, honest product slice that works end-to-end.

---

# Milestone 2 Objective

By Milestone 2, your team must demonstrate:

- One clearly defined MVP workflow
- Reliable retrieval for both definition queries and scenario queries
- Grounded answer generation with visible citations
- Validation that meaningfully checks the answer against retrieved data
- Correct refusal behavior when information is unsupported
- A working scenario engine that computes projections deterministically and explains results with citations
- A usable demo experience that another person can run
- Clear documentation of scope, quality, and known limitations

---

# 1. Required MVP Scope

Your MVP must fully support two primary workflows:

- Definition workflow: User selects a retirement topic or asks a definition question, receives a cited, validated explanation grounded to retrieved source chunks
- Scenario workflow: User enters personal financial inputs (age, retirement age, income, savings, monthly contribution), receives a deterministic projection with an LLM-generated explanation citing financial rules

Both workflows must be stable and demoable. If one path is fragile, declare one official MVP path and treat the other as stretch work.

## The MVP must support:

- Topic-aware retrieval from indexed sources (Northwestern Mutual PDF for definitions, Fidelity pages for numeric rules)
- Grounded answer generation using retrieved context
- Citation markers in every answer with traceable links to source documents
- Validation and repair loop that catches unsupported claims and regenerates
- Grounding verification that checks phrase-level overlap with source chunks
- Refusal when the answer is unsupported or the query falls outside indexed content
- Deterministic scenario projections with LLM explanation
- A demoable web UI (React frontend with FastAPI backend)

---

# 2. MVP Quality Bar

Your MVP is complete only if all of the following are true:

- Both workflows (definition and scenario) run end-to-end during demo without manual patching
- Definition answers work correctly for at least 5 retirement plan types (Roth IRA, 401(k), Traditional IRA, Rollover IRA, Roth 401(k))
- Scenario projections produce mathematically correct results matching the compound interest formula
- Every factual answer displays citation markers with working source links
- Unsupported answers are refused instead of guessed
- The validation and repair loop catches at least one class of error and regenerates
- The grounding verifier produces a phrase-level support report
- The README is sufficient for another team to run the system

---

# 3. Required Deliverables

Create or update the following:

- `/docs/MVP_definition.md`
- `/docs/Milestone_2_demo_script.md`
- `/docs/evaluation_test_cases.md` (updated)
- `/docs/risk_log.md`
- `/README.md` (updated)

Your repository must also include:

- The working application code (backend + frontend)
- `requirements.txt`
- `.env.example`
- A clearly identified launch command for both backend and frontend

---

# 4. MVP Definition Document

Create:

`/docs/MVP_definition.md`

This file must include:

- The exact MVP workflows selected (definition, scenario, or both)
- What a user can do in the MVP
- What is explicitly out of scope for Milestone 2
- Supported source types and their roles (PDF for definitions, web for numeric rules)
- Known limitations
- Definition of done for the MVP

Example:

> Users can select a retirement plan topic and receive a cited explanation grounded to verified financial sources, or enter personal financial inputs and receive a deterministic retirement projection with an LLM-generated explanation. All answers include citation markers linking to Northwestern Mutual or Fidelity. The system refuses to answer when no supporting source exists.

---

# 5. Demo Script

Create:

`/docs/Milestone_2_demo_script.md`

This file must include:

- Setup commands (backend and frontend)
- Run commands
- API key configuration instructions
- At least 5 demo questions covering both definition and scenario workflows
- At least 1 refusal-case question (query outside indexed content)
- The expected outcome for each question

The goal is reproducibility. Another person should be able to follow the script and obtain the intended demo.

---

# 6. Evaluation Update

Update:

`/docs/evaluation_test_cases.md`

Requirements:

- At least 20 test queries covering both definition and scenario workflows
- Include at least 3 refusal test cases (queries the system should decline)
- Include at least 2 scenario test cases with expected numerical outputs
- Fix the current gaps: every test case must show the actual generated answer text, not a placeholder like "According to Northwestern Mutual..."
- Include a short explanation of how each metric is computed

Required metrics:

- Retrieval accuracy (correct chunks retrieved for the query)
- Citation coverage (percentage of answers containing citation markers)
- Grounding accuracy (percentage of key phrases supported by retrieved chunks)
- Hallucination rate (percentage of answers containing claims not in source data)
- Refusal accuracy (percentage of unsupported queries correctly refused)

If there are failures, report them clearly and explain them honestly. Reporting 100% across all metrics with placeholder answers is not credible evaluation.

---

# 7. Validation Requirement

Your validation layer must be stronger than prompt-only grounding.

Current state: The team has a repair loop, citation format checking, and a phrase-level grounding verifier. For Milestone 2, these must all function together in the live pipeline.

Required improvements:

- The `extract_citation_phrases()` function must be actively used in validation (Sprint 1 noted it was unused)
- Citation validation must not rely on hardcoded source names (e.g., checking for "Northwestern" as a string)
- The grounding verifier must produce a visible report in the demo (not just a backend print statement)
- At least one deterministic check must verify that numeric claims in the answer (dollar amounts, percentages, age thresholds) appear in retrieved source chunks
- The repair loop must demonstrate at least one successful correction during the demo

If you continue using an LLM judge for any part of validation, you must justify why it is adequate and pair it with at least one deterministic check.

---

# 8. Scenario Engine Requirement

The scenario engine must be fully integrated by Milestone 2.

Required:

- The `/api/scenario` endpoint accepts user inputs and returns both a deterministic projection and an LLM explanation
- The LLM explanation must cite financial rules from retrieved Fidelity content
- The scenario engine must not use the LLM for any calculation
- Edge cases must be handled: zero savings, retirement age equal to current age, negative values, missing fields
- The frontend scenario form must display results clearly, including the projected balance and the explanation

The scenario engine is what separates this project from a generic term explainer. It must work.

---

# 9. Demo Experience Requirement

You must provide a usable demo interaction through your React frontend.

At minimum:

- The evaluator can select a retirement topic and receive a cited definition
- The evaluator can enter scenario inputs and receive a projection with explanation
- The evaluator can see citation markers that link to source documents
- The evaluator can see the validation status (validated vs. corrected)
- The evaluator can see the grounding support (supported phrases)
- The evaluator can trigger a refusal case

For Milestone 2, usability matters more than visual polish. But the UI must not require verbal coaching to operate.

---

# 10. Repository Requirements

By Milestone 2, the repository must include:

- A corrected and complete README with setup and run instructions for both backend and frontend
- `requirements.txt` (currently missing from the repo)
- `.env.example` (currently missing from the repo)
- Consistent file names referenced by deliverable docs
- No hard-coded API keys (the current `input()` prompt for API key is acceptable, but `.env.example` must document the expected variable)
- No committed `.env` files or virtual environments (verify `.gitignore` covers these)
- Evidence of team contributions in commit history (currently heavily skewed to 1-2 contributors)
- Clear labeling of prototype-only files

If a required artifact lives outside the repo, link it from the repo.

---

# Required Live Demo Video for Milestone 2

You must demonstrate:

1. Launching the MVP from a clean starting point (backend + frontend)
2. Selecting a retirement topic and receiving a cited definition
3. Showing the retrieved chunks that support the answer
4. Showing citation markers and their source links
5. Showing the validation status and grounding report
6. Entering scenario inputs and receiving a deterministic projection with explanation
7. Showing at least one correct refusal case (unsupported query)
8. Showing the repair loop correcting an answer (or explaining when it triggers)
9. Explaining one known limitation honestly

If the demo only works with instructor help, the MVP is incomplete.

---

# Milestone 2 Standard

Your project must evolve from:

"We have a RAG pipeline with citation formatting and a scenario formula."

To:

"We have a narrow but credible retirement planning MVP that another person can run, test, and trust within its stated scope, with verifiable citations, deterministic projections, and honest refusal behavior."
