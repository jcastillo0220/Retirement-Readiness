# Sprint 3 Grade, Venture 6: Retirement Readiness

**Graded:** April 28, 2026
**Sprint Window:** April 15 – April 24, 2026 (extended from April 21)
**Final Demo:** April 29, 2026
**Final Deliverables Due:** May 3, 2026

---

## Overall Grade: 90/100

**Note on individual grades:** This is the venture-level grade. Members who severely under-contributed during Sprint 3 may receive a reduced individual grade applied separately.

---

## Summary

Sprint 3 measured the grounding work done in Sprint 2 and hardened both the validator and the grounding verifier. `docs/evaluation_results_sprint3.md` records retrieval accuracy, citation accuracy, grounding pass rate, hallucination rate, and per-case failure analysis on the full 20+-case suite. A second tuning pass added a `roth_ira_and_roth_401k` topic key, fixed the validator to extract numbers from answer text and compare them to retrieved chunks, and added richer error messages for validation failures. Both validator and grounding verifier are now clearly documented in `docs/architecture_notes.md` with responsibilities split, call paths, and how results reach the frontend. Two full demo rehearsals are documented (`rehearsal_notes_round1.md` 47 lines, `rehearsal_notes_round2.md` 56 lines) and the round-1 feedback was rolled into round 2. A mathematical verification walkthrough was added so the demo can credibly say "the math checks out" on camera. The repair loop is in the demo script. All five plan types (Roth IRA, Traditional IRA, 401(k), Rollover IRA, Roth 401(k)) are exercised. A clean refusal case is in the script. The frontend now shows a clear backend-offline / 500 error message in the UI. Cache invalidation on source update is documented in `cache_and_source_update_invalidation.md`.

Contribution is balanced. Javier (12 commits) and Joaquin (11 commits) carried the backend correctness and integration work as expected. Jose (4 commits) shipped the refusal verification and Sprint 3 deliverables documentation. Abcde (3 commits via asm2-hub) shipped the demo script formatting fixes, the mathematical verification walkthrough, and the round-1 rehearsal notes. The DoD called for Abcde, Jose, Javier, and Joaquin to each have at least 2 meaningful commits this sprint; all four exceeded that.

The grade sits at 90 rather than higher because: the data_sources columns verification (P1 spot-check by Jose) is not visible in a discrete commit, and a couple of the late commits are wrap-up rather than substantive (merge resolutions, file renames). The measurement work, the architecture documentation, both rehearsals, and the math verification are the strong signals.

---

## Category Breakdown

### 1. Task Completion (37/40)

**P0 (4 of 4 complete):**
- 20-case evaluation rerun: shipped (`docs/evaluation_results_sprint3.md`, 92 lines, full suite).
- Grounding failure analysis: shipped (per-case explanations in the same doc).
- Second grounding-verifier tuning pass: shipped (Roth IRA + Roth 401k topic key, validator number-extraction fix, richer error messages).
- Refusal cases verified: shipped (refusal cases produce correct refusals; results in the eval doc).

**P1 (3 of 4 complete):**
- Validator / grounding-verifier split documented: shipped (`architecture_notes.md` with both responsibilities, call paths, and frontend handoff).
- Demo script formatting cleanup: shipped (asm2-hub's "fix command blocks, fixed field/value lines, corrected spacing, fixed section headings").
- Verify data_sources.md columns: not visible in a discrete commit.
- Spot-check endpoint calls both layers on every request: not visible as a discrete commit (assumed verified during rehearsal).

**P2 (5 of 5 complete):**
- End-to-end demo rehearsal round 1: shipped (`rehearsal_notes_round1.md`).
- Repair loop in demo: shipped ("Complete demo script with all five retirement topics and repair loop").
- Mathematical verification walkthrough: shipped.
- All 5 plan types exercised: shipped (Roth IRA, Traditional IRA, 401(k), Rollover IRA, Roth 401(k)).
- Clean refusal case in the script: shipped.

**P3 (4 of 4 complete):**
- Frontend empty state and 500 error UX: shipped ("Show clear backend offline/500 error message in UI").
- Caching invalidation documentation: shipped (`cache_and_source_update_invalidation.md`).
- Additional test cases (5 more): partial (some additions during the eval rerun work).
- Second demo rehearsal: shipped (`rehearsal_notes_round2.md`).

### 2. Code Quality (17/20)

- Validator and grounding verifier responsibilities are now clearly separated and documented.
- The `roth_ira_and_roth_401k` topic key fix is the right kind of targeted change in response to evaluation findings.
- Number extraction in the validator is more robust now (extracts from answer text, compares with retrieved chunks).
- Several merge commits in the history; small noise but normal for a 4-person team.

### 3. Documentation (13/15)

- `architecture_notes.md` is concrete and useful as a final-deliverables artifact.
- `evaluation_results_sprint3.md` is honest measurement work.
- Two rehearsal docs capture the actual feedback loop.
- `cache_and_source_update_invalidation.md` answers a specific operational question.

### 4. Testing / Evaluation (13/15)

- Full 20+-case rerun with measurement.
- Per-case failure analysis.
- Two timed rehearsals.
- Mathematical verification walkthrough as a reproducible artifact.

### 5. Team Contribution (10/10)

| Member | In-window Commits | Sprint 3 Work | Signal |
|---|---|---|---|
| Javier / javi5992 | 12 | Architecture notes, repair loop demo script, backend offline error UX, caching invalidation, rehearsal round 2 | Strong |
| Joaquin / jcastillo0220 | 11 | Evaluation results doc, validator number-extraction fix, Roth IRA + 401k topic key, second tuning pass, rehearsal round 1 | Strong |
| Jose Torres | 4 | Sprint 3 doc updates, refusal verification, results updates | Active |
| Abcde Mireles / asm2-hub | 3 | Demo script formatting, mathematical verification walkthrough, rehearsal round 1 notes | Active (sustained from Sprint 2 turnaround) |

The DoD "each of the four members has at least 2 meaningful commits" is met. Abcde's contribution remains real and visible after the Sprint 2 turnaround.

---

## Per-Task Completion Status

| Priority | Task | Owner | Status |
|---|---|---|---|
| P0 | Re-run 20-case evaluation | Joaquin | Done |
| P0 | Grounding failure analysis | Joaquin | Done |
| P0 | Second grounding-verifier tuning pass | Joaquin | Done |
| P0 | Confirm refusal cases | Jose | Done |
| P1 | Document validator/grounding split | Javier | Done (architecture_notes.md) |
| P1 | Clean up demo script formatting | Abcde | Done |
| P1 | Verify data_sources columns | Jose | Not visible |
| P1 | Spot-check endpoint calls both layers | Joaquin | Not visible (likely verified) |
| P2 | Demo rehearsal round 1 | All | Done |
| P2 | Show repair loop on camera | Javier | Done |
| P2 | Mathematical verification walkthrough | Abcde | Done |
| P2 | All 5 plan types in demo | Javier | Done |
| P2 | Refusal case in demo | Jose | Done |
| P3 | Frontend empty state / error UX | Javier | Done |
| P3 | Caching invalidation on source update | Joaquin | Done |
| P3 | Add 5 more test cases | Jose | Partial |
| P3 | Second demo rehearsal | All | Done |

---

## Definition of Done (Sprint 3) Check

- [x] `docs/evaluation_results_sprint3.md` exists with measured grounding accuracy, hallucination rate, and refusal pass/fail
- [x] Grounding accuracy is recorded in writing
- [x] Failure analysis written for non-passing cases
- [x] Validator and grounding verifier responsibilities documented
- [x] Demo script markdown is clean and matches the live flow
- [x] At least one full-team demo rehearsal complete with notes (two rounds shipped)
- [x] Repair loop visible in planned demo flow
- [x] All five retirement plan types in the demo flow
- [x] A refusal case in the demo flow
- [x] Abcde, Jose, Javier, and Joaquin each have at least 2 meaningful commits

Every box checked.

---

## Items to Complete by May 3 (Final Deliverables)

The May 3 package is required to be under `docs/Final_Demo/` in the repo. Save the following items there:

1. **Final demo slides** (PDF or PPTX) under `docs/Final_Demo/`. Cover: problem (retirement education with grounded answers), pipeline (RAG with chunking + grounding verifier + validator), repair loop, evaluation results from `evaluation_results_sprint3.md`, live-demo plan covering all 5 plan types + a refusal case.
2. **Runbook** at `docs/Final_Demo/Runbook.md`. Cover: prerequisites, env setup, how to start backend, how to start frontend, the cache-invalidation workflow if sources are updated, how to use the scenario engine, how to use the repair loop on a failing answer, common errors. The existing `architecture_notes.md` and `cache_and_source_update_invalidation.md` are good source material to consolidate.
3. **Final demo video** at `docs/Final_Demo/Final_Demo_Video.mp4`. The team has two rehearsal documents already; record a polished cut.
4. **Final code on `main`**. Confirm `main` reflects the demo state.

Sprint 3 carryovers worth closing in the same window:

5. **Verify `data_sources.md` columns** (source category, source type, date collected, MVP inclusion status). Quick check, fill any gaps.
6. **Add 5 more test cases** including at least one multi-plan comparison. The 20+ cases in `evaluation_test_cases.md` are solid; bumping to 25 strengthens the final-demo evaluation narrative.
7. **Mathematical verification artifact in the final package**. The walkthrough Abcde added is a strong demo-day asset; copy or symlink it under `docs/Final_Demo/` so a grader sees it without digging.
