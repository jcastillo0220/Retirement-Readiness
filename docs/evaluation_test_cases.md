# Retirement Readiness — Evaluation Test Cases

## Standard Test Cases

| # | User Query | Expected Source Document | Retrieved Documents | Generated Answer | Citation Verification | Grounding Check |
|---|------------|--------------------------|---------------------|------------------|-----------------------|-----------------|
| 1 | What is a Roth IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 2 | What is a 401(k)? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 3 | What is a Roth 401(k)? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 4 | What is a rollover IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 5 | What is a traditional IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 6 | How do taxes work in a Roth IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 7 | What are qualified withdrawals? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 8 | What are contribution limits? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 9 | Roth vs Traditional IRA | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 10 | How does a 401(k) work? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 11 | What are 401(k) tax rules? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 12 | How are Traditional IRAs taxed? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 13 | Traditional IRA contribution rules | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 14 | When to use a Rollover IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |
| 15 | Roth 401(k) vs Roth IRA | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | According to Northwestern Mutual... | Northwestern Mutual PDF | Pass |

> **Fix note — rows 18 & 19 (original):** The original test case table had the queries for rows 18 and 19 swapped. Row 18 ("When to use a Rollover IRA?") was mapped to the Roth 401(k) answer, and row 19 ("What is a Roth 401(k)?") was mapped to the Rollover IRA answer. Both have been corrected and renumbered as rows 14 and 15 above.

---

## Refusal Test Cases

The system should refuse or clearly disclaim answers for queries that are out of scope, unrelated to retirement, or have no supporting source content. In all refusal cases the expected behavior is the same: the system should **not** fabricate a grounded answer, should **not** cite a source it did not use, and should return either a clear disclaimer or a polite out-of-scope message.

| # | User Query | Query Type | Expected Behavior | Expected Source | Citation Expected | Grounding Check | Pass Condition |
|---|------------|------------|-------------------|-----------------|-------------------|-----------------|----------------|
| R-01 | What stocks should I buy right now? | Out-of-scope — investment advice | System returns a disclaimer stating it only covers retirement account education, not live investment recommendations. No source is cited. | None | No | N/A — refusal expected | Pass if no source is cited and a clear scope disclaimer is returned |
| R-02 | What is the best recipe for banana bread? | Non-retirement question | System returns a polite message that the question is outside the scope of the retirement assistant. No answer is generated. | None | No | N/A — refusal expected | Pass if the system does not attempt to answer and returns an out-of-scope message |
| R-03 | What will the stock market do next year? | No supporting source — speculative financial query | System returns a general knowledge disclaimer noting that no project sources support a forward-looking market prediction, and declines to speculate. No source is cited. | None | No | N/A — refusal expected | Pass if the answer contains a disclaimer and does not cite any loaded source |

---

## Required Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Retrieval Accuracy | 100% | Correct source retrieved for every in-scope query |
| Citation Accuracy | 100% | Every citation matches the actually retrieved source |
| Grounding Pass Rate | 100% | Answer content supported by retrieved chunks |
| Refusal Accuracy | 100% | Out-of-scope and unsupported queries correctly refused or disclaimed |