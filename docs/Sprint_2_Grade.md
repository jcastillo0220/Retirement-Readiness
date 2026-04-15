# Sprint 2 Grade — Venture 6: Retirement Readiness

**Graded:** April 15, 2026
**Sprint Window:** April 8 – April 14, 2026
**Final Demo:** April 29, 2026

---

## Overall Grade: 87/100

---

## Summary

Retirement Readiness had a productive Sprint 2. Both P0 critical bugs from Milestone 2 are fixed, the missing demo script exists, three refusal test cases are documented, scenario test cases 18/19 were corrected, PRD.pdf was converted to PRD.md, the empty `data_sources/PRD.pdf` was removed, and IRS data sources plus a real chunking-overlap change landed. Most importantly, Abcde Mireles moved from 4 commits over the entire project to 7 commits in one week on concrete, meaningful work (chunking overlap in `backend/chunking.py`, IRS data ingestion, PRD conversion, demo script, file cleanup). That is a real turnaround.

The main gap: there is no recorded measurement of the new grounding accuracy or hallucination rate. Sprint 2 was supposed to push grounding from 48.3% toward 70% and get a number written down. The code changes that should move the needle are in place (cleaner `grounding_verifier.py`, chunking overlap, out-of-scope keyword detection in `chunking.py`), but nobody re-ran the 20-case eval and logged the results. A number is needed before the final demo.

Also worth noting: the validator phrase-level "dead code" was not wired back in. Instead `validator.py` was simplified and the phrase grounding checks now live entirely in `grounding_verifier.py`, with the endpoint surfacing the grounding report separately. This is a legitimate architectural choice and the scenario endpoint tuple-unpacking crash is clearly fixed (`endpoint.py` lines 456–461 and 597–598 now guard both tuple and list returns), but the team should document the split so it is not read as "still broken" at final grading.

---

## Category Breakdown

### 1. Task Completion (34/40)

**P0 — Critical Bug Fixes**
- Fix validator dead code: **Partial.** `validator.py` now correctly appends `unsupported_nums` to the errors list and returns `{"valid": False}` when numeric claims are not found in chunks (lines 131–148). Phrase-level "unsupported" check was not wired into the validator; instead the phrase grounding logic was moved entirely to `grounding_verifier.py` and consumed separately in the endpoint. This is acceptable but deviates from the Sprint 2 task as written.
- Fix scenario endpoint crash: **Done.** Both `verify_answer_grounding()` call sites (`endpoint.py` lines 456–461 and 597–598) now handle both tuple and list returns defensively. Scenario route will no longer crash at runtime.
- Fix eval test cases 18/19: **Done.** `evaluation_test_cases.md` now has the corrected mapping as rows 14/15 with an explicit "Fix note" explaining the original swap.

**P1 — Missing Deliverables**
- Write demo script: **Done.** `Milestone_2_Demo_Script.md` (174 lines) covers prerequisites, backend/frontend setup, and 6 demo scenarios including a fallback case. Formatting has some minor artifacts (e.g. "bashgit clone", line 128 field values concatenated) that should be cleaned up for final.
- Add refusal test cases: **Done.** Three refusal cases (R-01 out-of-scope investment advice, R-02 banana bread, R-03 market speculation) are documented in `evaluation_test_cases.md` with expected behavior and pass conditions.
- MVP_definition.md late note: **Done.** MVP_definition.md was updated (cc6df50).

**P2 — Grounding Accuracy Improvement**
- Analyze grounding failures: **Not documented.** No written analysis of the 48.3% / 15% failure patterns exists in `docs/`.
- Tune grounding verifier: **Partial.** `grounding_verifier.py` was significantly rewritten (52 → 193 lines) with a new `clean_answer_for_grounding()` step, better phrase extraction, and more structured numeric claim checking. Likely improves accuracy, but no post-tuning number is recorded anywhere.
- Reduce hallucination rate: **Partial.** Generation prompt tightening is visible in the validator repair prompt and answer-cleaning logic. Again, no measured post-fix hallucination rate.
- Expand data sources: **Done.** IRS data source content was added (7e0f94b by Abcde).
- Improve chunking strategy: **Done.** `backend/chunking.py` now includes chunk overlap logic and an `OUT_OF_SCOPE_KEYWORDS` list used to short-circuit off-topic queries before retrieval (79ca635, 56d5ca9).

**P3 — Polish & Documentation**
- Complete `data_sources.md`: **Partial.** File exists under `docs/data_sources/` but the specific column additions (source category, source type, date collected, MVP inclusion status) were not verified as fully present.
- Update PRD: **Done.** `PRD.md` was modified twice by Javier on Apr 14 with scope clarifications. Grounding target listed as "≥ 70%".
- Convert PRD.pdf to PRD.md: **Done.** `docs/PRD.md` exists (166 lines) (eb06d0a by Abcde).
- Remove empty data_sources/PRD.pdf: **Done.** (27e8ae3 by Abcde).
- Demo rehearsal: **Not verified.** No artifact confirms this happened.

### 2. Code Quality & Architecture (17/20)

- Both P0 runtime bugs are fixed. The endpoint now defends against both tuple and list returns from `verify_answer_grounding()`, which is a good defensive pattern.
- `grounding_verifier.py` rewrite cleanly separates word normalization, answer cleaning, phrase supporting, and numeric claim checking. Good modular progress.
- `chunking.py` adds an out-of-scope keyword filter that will actually help refusal cases work deterministically before any LLM call.
- `validator.py` is simpler and the numeric cross-check is now load-bearing instead of dead.
- **Concern:** The validator no longer imports phrase-level helpers from `grounding_verifier`. The split is fine, but `endpoint.py` must make sure both layers are actually called on every response. This should be spot-checked in Sprint 3.
- **Concern:** Some commits are still bare "modified: <file>" messages with no description. Please write real commit messages.

### 3. Documentation (13/15)

- Demo script exists and is usable. Some markdown formatting artifacts should be cleaned.
- PRD.md now exists as the source of truth for the product.
- evaluation_test_cases.md covers refusal scenarios and documents the 18/19 fix.
- **Missing:** No written grounding-failure analysis, no post-tuning metrics, no "we re-ran the eval and got X%" note.

### 4. Testing & Evaluation (10/15)

- Refusal test cases are documented on paper with clear pass conditions.
- Standard test cases 18/19 are fixed.
- **Missing:** Actual measured grounding accuracy and hallucination rate after the grounding verifier and chunking changes. This was the single biggest P2 deliverable and the number is not in the repo. Without it we cannot say whether Sprint 2's grounding work actually moved the metrics.

### 5. Team Contribution (9/10)

- Joaquin Castillo (jcastillo0220): 3 commits. Fixed the `endpoint.py` bug, added grounding report back to the frontend with source badges, fixed the answer/answer_body field plumbing. Volume is lower than Milestone 2 but the commits address the exact P0 owners assigned.
- Javier Castillo (javi5992): 4 commits. Updated PRD.md twice, merged main, updated MVP_definition.md. Leadership work visible.
- Jose Torres: 4 commits. Tried to help with validation, updated chunking, renamed a previously submitted file, merged main.
- **Abcde Mireles (asm2-hub): 7 commits.** Added IRS data sources, improved chunking strategy with overlap, converted PRD to markdown, removed the empty PRD.pdf, updated demo script. **This is the biggest Sprint 2 win for team health.** The concrete P3 assignments worked. Keep this up for Sprints 3 and 4.

The contribution pattern shifted meaningfully. The heavy-lifters (Joaquin, Javier) did fewer commits this week but they fixed the P0 bugs, which is exactly the right prioritization. Abcde's turnaround removes the severe-imbalance red flag as of this sprint, provided the momentum continues.

---

## Individual Contribution Summary (Red Flag Indicator)

| Team Member | Sprint 2 Commits | Notes |
|---|---|---|
| Joaquin Castillo | 3 | P0 endpoint fix plus frontend plumbing. High-impact. |
| Javier Castillo | 4 | PRD and MVP doc updates, integration work. |
| Jose Torres | 4 | Validation and chunking assists, file cleanup. |
| Abcde Mireles | 7 | IRS sources, chunking overlap, PRD conversion, demo script, cleanup. Strong turnaround from M2. |

Per course policy, individual grades are a red flag indicator only. The venture-level grade (87) applies to every team member unless a contribution issue is formally raised. **No red flag for Sprint 2.** Abcde's Sprint 2 work clears the Milestone 2 concern provided Sprints 3 and 4 continue at this level or better.

---

## Key Wins

1. Both P0 critical bugs from Milestone 2 are fixed. The scenario endpoint will no longer crash, and the validator's numeric cross-check is load-bearing.
2. Abcde Mireles delivered 7 meaningful commits across data, chunking, PRD, and cleanup. Real turnaround.
3. Demo script, refusal test cases, PRD.md, and eval 18/19 fix are all in place. The Milestone 2 paperwork gaps are closed.

## Key Gaps Going Into Sprint 3

1. **No measured grounding accuracy or hallucination rate post-tuning.** The whole point of the P2 block was to move from 48.3% toward 70% and write the number down. Re-run the 20-case eval in Sprint 3, week 1.
2. **No written grounding-failure analysis.** Sprint 2 asked for "top failure patterns" so the team understands *why* accuracy was low. This is still needed.
3. **Demo script polish.** The current script has markdown artifacts ("bashgit clone", concatenated field values on line 128). Clean this before rehearsal.
4. **Validator/grounding split not documented.** The endpoint now leans on `grounding_verifier.py` rather than the validator for phrase-level grounding. Add a one-paragraph note to the README or architecture doc so a reviewer can trace the decision path.
5. **Demo rehearsal not confirmed.** Do at least one full dry run before Sprint 4.

---

## Recommendations for Sprint 3

See `docs/Sprint 3.md`.
