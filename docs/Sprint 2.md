# Sprint 2 Plan — Venture 6: Retirement Readiness

**Sprint Duration:** April 8 – April 14, 2026
**Sprint Goal:** Fix critical bugs, write missing demo script, add refusal test cases, and improve grounding accuracy.
**Final Demo:** April 29, 2026

---

## Context

After Milestone 2, Retirement Readiness has two working workflows (definition RAG + scenario projections) with a polished React frontend showing citations, grounding reports, and validation status. However, there are two critical code bugs (validator dead code, scenario endpoint crash), a missing demo script, no refusal test cases, and a 48.3% grounding accuracy / 15% hallucination rate that need significant improvement. Sprint 2 focuses on fixing bugs and strengthening grounding quality.

---

## Sprint 2 Tasks

### P0 — Critical Bug Fixes (Days 1–2)

| Task | Owner | Description |
|---|---|---|
| Fix validator dead code | Joaquin | In `validator.py`, `unsupported` phrases and `unsupported_nums` are computed but never added to the `errors` list. Fix so they affect the valid/invalid decision |
| Fix scenario endpoint crash | Joaquin | In `endpoint.py` line 482, `verify_answer_grounding()` returns a list but code tries tuple unpacking. Fix the return handling |
| Fix eval test cases 18/19 | Jose | Scenario test cases 18 and 19 have swapped generated answers. Correct the mapping |

### P1 — Missing Deliverables (Days 2–3)

| Task | Owner | Description |
|---|---|---|
| Write demo script | Javier | Create `/docs/Milestone_2_demo_script.md` with demo order, exact questions, expected screen behavior, refusal example, and backup questions |
| Add refusal test cases | Jose | Add at least 3 refusal test cases to evaluation: out-of-scope query, non-retirement question, query with no supporting source |
| Submit MVP_definition.md note | Javier | Acknowledge in docs that MVP_definition.md was submitted late (4/6) |

### P2 — Grounding Accuracy Improvement (Days 3–6)

| Task | Owner | Description |
|---|---|---|
| Analyze grounding failures | Joaquin | Review the 48.3% grounding accuracy — identify top failure patterns. Are phrases being too aggressively extracted? Is the overlap threshold (50%) too strict? |
| Tune grounding verifier | Joaquin | Adjust phrase extraction and overlap thresholds. Target ≥70% grounding accuracy |
| Reduce hallucination rate | Javier | Analyze the 15% hallucination cases. Tighten the generation prompt, reduce temperature further if needed, add more explicit constraints |
| Expand data sources | Abcde | Add more retirement source content (e.g., additional Fidelity pages, IRS publication excerpts) to improve retrieval coverage |
| Improve chunking strategy | Jose | Experiment with chunk size and overlap in `chunking.py` to improve retrieval relevance |

### P3 — Polish & Documentation (Days 5–7)

| Task | Owner | Description |
|---|---|---|
| Complete data_sources.md | Jose | Add required columns: source category, source type, date collected, MVP inclusion status |
| Update PRD | Javier | Add scenario workflow, current acceptance metrics, and scope clarifications |
| Convert PRD.pdf to PRD.md | Abcde | Convert to markdown for repo consistency |
| Fix empty data_sources/PRD.pdf | Abcde | Remove the 0-byte file or replace with actual content |
| Demo rehearsal | All | Full team run-through of both workflows + refusal case |

---

## Definition of Done (Sprint 2)

- [ ] Validator phrase-level checks actually affect the valid/invalid outcome
- [ ] Scenario endpoint runs without crashing
- [ ] `Milestone_2_demo_script.md` exists with complete demo flow
- [ ] At least 3 refusal test cases documented with results
- [ ] Grounding accuracy improved from 48.3% toward ≥70%
- [ ] Hallucination rate reduced from 15% toward ≤5%
- [ ] Each team member has code commits this sprint (especially Abcde)

---

## Contribution Expectations

Joaquin (103 commits) and Javier (77 commits) account for 87% of all work. **Abcde Mireles has only 4 commits across the entire project** — this is critically below expectations. Sprint 2 assigns Abcde concrete tasks (data source expansion, PRD conversion, file cleanup). Jose should continue ramping up. All team members must have meaningful code contributions.

---

## Remaining Sprints Overview

| Sprint | Dates | Focus |
|---|---|---|
| Sprint 2 (this sprint) | Apr 8–14 | Bug fixes, missing deliverables, grounding accuracy |
| Sprint 3 | Apr 15–21 | Feature refinement, UI polish, demo rehearsal |
| Sprint 4 | Apr 22–28 | Final integration, presentation prep, final deliverables |
| **Final Demo** | **Apr 29** | **Presentation and live demo** |
| Final Deliverables Due | May 3 | All documentation and code finalized |
