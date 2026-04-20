# Sprint 3 Plan — Venture 6: Retirement Readiness

**Sprint Duration:** April 15 – April 21, 2026
**Sprint Goal:** Measure the grounding improvements, close remaining Sprint 2 gaps, harden both workflows, and run a full demo rehearsal so Sprint 4 can focus on polish and presentation prep.
**Final Demo:** April 29, 2026

---

## Context

Sprint 2 cleared the Milestone 2 paperwork gaps (demo script, refusal test cases, PRD.md, test case 18/19 fix) and fixed both P0 runtime bugs in `endpoint.py` and `validator.py`. The grounding verifier was rewritten and chunking now includes overlap plus an out-of-scope keyword filter. Abcde Mireles turned a serious contribution concern around with 7 Sprint 2 commits.

The biggest open item is measurement. The grounding-verifier rewrite and chunking overlap are likely better, but nobody re-ran the 20-case evaluation, so we cannot say whether the 48.3% grounding accuracy or 15% hallucination rate actually moved. Sprint 3 must produce that number in writing. Sprint 3 also needs to polish the demo script, lock down the validator vs grounding verifier split, and confirm every PRD feature works end-to-end in a rehearsal.

---

## Sprint 3 Tasks

### P0 — Measure and Lock In Grounding Gains (Days 1–3)

| Task | Owner | Description |
|---|---|---|
| Re-run 20-case evaluation | Joaquin | Run all 15 standard test cases plus 3 scenario cases plus 3 refusal cases against the current backend. Record retrieval accuracy, citation accuracy, grounding pass rate, hallucination rate. Commit results to `docs/evaluation_results_sprint3.md` |
| Write grounding failure analysis | Joaquin | For every case that fails grounding, write one sentence explaining why (phrase too aggressive, chunk missing, number paraphrased, etc.). Add as a section in `evaluation_results_sprint3.md` |
| Second grounding-verifier tuning pass | Joaquin | Based on the failure analysis, adjust thresholds or phrase extraction in `grounding_verifier.py`. Re-run the eval. Commit a before/after comparison |
| Confirm refusal cases actually refuse | Jose | Run R-01, R-02, R-03 through the live backend. Capture the response text for each and paste into `evaluation_results_sprint3.md`. If any refusal produces a grounded answer instead, file it as a bug and fix in this sprint |

### P1 — Close Remaining Sprint 2 Gaps (Days 1–3)

| Task | Owner | Description |
|---|---|---|
| Document validator/grounding split | Javier | Add a short "Validation Architecture" section to README or a new `docs/architecture_notes.md` explaining: validator handles citation format and numeric cross-check; grounding_verifier handles phrase-level support; both are surfaced to the frontend. Include the call path for a single request |
| Clean up demo script formatting | Abcde | Fix markdown artifacts in `Milestone_2_Demo_Script.md`: separate "bash" from commands, break line 128 into a real field-by-field table, fix any other concatenated lines. Re-read as a fresh developer |
| Verify data_sources.md columns | Jose | Confirm `docs/data_sources/data_sources.md` has the four required columns: source category, source type, date collected, MVP inclusion status. Fill in any missing columns |
| Spot-check endpoint still calls both layers | Joaquin | Add one print or log line per request confirming both `validate_answer()` and `verify_answer_grounding()` are called on every non-cached response. Remove the logging before final demo |

### P2 — Final Demo Hardening (Days 3–5)

| Task | Owner | Description |
|---|---|---|
| End-to-end demo rehearsal round 1 | All | Full 8–10 minute run-through following `Milestone_2_Demo_Script.md`. Both team laptops, one as backup. Time it. Note every UI glitch, every awkward pause. Commit a `docs/rehearsal_notes_round1.md` |
| Show the repair loop on camera | Javier | Sprint 2 did not demo the repair loop. Craft a question that will reliably trigger a first-pass validation failure and a successful repair. Add it as scenario 7 in the demo script |
| Walk through mathematical verification | Abcde | Pick one scenario input (e.g. age 25, retire at 65, $500/month, 7% return). Compute the expected balance by hand or spreadsheet and add the expected number next to the demo scenario in the script so the demo can say "and the math checks out" on camera |
| Show all 5 plan types | Javier | Make sure the demo flow visits Roth IRA, Traditional IRA, 401(k), Rollover IRA, and Roth 401(k). The M2 video only showed some |
| Add a proper content-grounding refusal | Jose | The M2 demo did not show a clean refusal. Pick R-02 (banana bread) or similar and put it in the script as a live refusal case |

### P3 — Stretch and Polish (Days 5–7)

| Task | Owner | Description |
|---|---|---|
| Frontend empty state and error UX | Javier | Verify the UI handles a backend error gracefully (network drop, 500). Currently unknown — test it |
| Caching invalidation on source update | Joaquin | Confirm that if chunks are re-loaded the in-memory cache does not serve stale answers. Document the behavior |
| Add 5 more test cases | Jose | Expand from 20 to 25 cases to strengthen the evaluation story. Include at least one multi-plan comparison |
| Second demo rehearsal | All | Day 7 run-through incorporating round 1 notes. Commit `docs/rehearsal_notes_round2.md` |

---

## Definition of Done (Sprint 3)

- [ ] `docs/evaluation_results_sprint3.md` exists with measured grounding accuracy, hallucination rate, and refusal pass/fail for every case
- [ ] Grounding accuracy is recorded in writing, whatever the number. Target is still ≥70% but measurement matters more than the number this week
- [ ] Failure analysis written for every non-passing case
- [ ] Validator and grounding verifier responsibilities are documented in the repo
- [ ] Demo script markdown is clean and matches the live flow
- [ ] At least one full-team demo rehearsal is complete with notes committed
- [ ] Repair loop is visible in the planned demo flow
- [ ] All five retirement plan types are in the demo flow
- [ ] A refusal case is in the demo flow
- [ ] Abcde, Jose, Javier, and Joaquin each have at least 2 meaningful commits this sprint

---

## Contribution Expectations

Sprint 2 removed the severe-imbalance red flag thanks to Abcde's turnaround (7 commits). Keep that pattern. Every team member should land at least 2 meaningful commits this week. Heavy-lifters Joaquin and Javier should continue owning the backend correctness and integration work. Jose should own refusal verification and test case expansion. Abcde should own the demo script cleanup and mathematical verification artifact — both are concrete and visible.

If any team member cannot commit code in a given week, they should explicitly log the design, research, or pair-programming work they did instead, either in a sprint note or in the team's standup channel. Commit counts alone do not capture contribution, but silence does raise flags.

---

## Remaining Sprints Overview

| Sprint | Dates | Focus |
|---|---|---|
| Sprint 2 (done) | Apr 8–14 | Bug fixes, missing deliverables, grounding code changes |
| Sprint 3 (this sprint) | Apr 15–21 | Measurement, demo hardening, rehearsal round 1 |
| Sprint 4 | Apr 22–28 | Final polish, rehearsal round 2, presentation prep |
| **Final Demo** | **Apr 29** | **Presentation and live demo** |
| Final Deliverables Due | May 3 | All documentation and code finalized |

---

## Risks to Watch

1. **Grounding number might still be low.** That is fine for Sprint 3 as long as the number is measured and documented. Sprint 4 can do one more tuning pass if needed. Do not hide a bad number.
2. **Repair loop may not trigger reliably on demand.** Have a backup question ready if the primary one gets repaired on first pass.
3. **Demo timing.** The script has 6 scenarios plus refusal plus scenario engine plus repair loop. Time the rehearsal and cut whatever pushes past 10 minutes.
4. **Cache serving stale answers during demo.** Clear the cache before the live demo. Add a note to the demo script.

---

## Final Demo Day Heads-Up (April 29)

Two weeks out. Rehearse toward this format during Sprint 3 and Sprint 4.

**12 minutes per team, hard cap.** I will cut you off at 12:00 to keep all 8 teams on schedule, so rehearse to 10:30 or 11:00 to leave margin. Suggested split:

1. **About 3 min: overall design.** What the product does, the core pipeline, and the architectural decisions that matter (retrieval strategy, validator or grounding approach, refusal policy). No code walkthroughs.
2. **About 4 min: individual contributions.** Every team member speaks briefly about what they personally owned this semester. Plan what you will say, roughly 45 to 60 seconds each.
3. **About 4 min: live demo of the highlights.** Pick 2 or 3 scenarios from your existing demo script. Required: at least one refusal or failure case and at least one end-to-end grounded answer. Do not spend this time on UI polish.
4. **About 1 min: Q&A**, included in the 12 minutes.

**Running order** is Venture 1 through Venture 8 in order, so Retirement Readiness presents sixth.

**Backup plan:** have a prerecorded screen capture of the working path ready in case the live demo fails. Internet or API hiccups are not an excuse on demo day.

**Slides and runbook:** not due before the presentation, but both are required artifacts in the final deliverables package due May 3. Save them under `docs/Final_Demo/` in your repo.

**Avoid:** narrating code, reading slides verbatim, skipping the refusal case, opening with missing features. Present the version you are proud of.

Rehearse the full 12 minutes end to end at least twice, at least once with a timer.
