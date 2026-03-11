# Retirement QA Evaluation Matrix

This document includes:

- 20 retirement‑related queries
- Expected source documents
- Retrieved documents
- Generated answers
- Citation verification results
- Grounding pass/fail
- Required evaluation metrics

---

## Test Cases 1–2 (Definition Queries)

| # | User Query | Requirement Type | Expected Source Document | Retrieved Documents | Generated Answer | Citation Verification | Grounding Check | Pass/Fail |
|---|------------|------------------|---------------------------|----------------------|-------------------|------------------------|------------------|-----------|
| 1 | What is a Roth IRA? | Definition | Roth IRA PDF | | | Expected: Roth IRA PDF | | |
| 2 | What is a 401(k)? | Definition | 401(k) PDF | | | Expected: 401(k) PDF | | |

---

## Test Cases 3–20 (Numeric / Explanation Queries)

| Test Case | User Query | Requirement Type | Expected Source Document | Retrieved Documents | Generated Answer | Citation Verification | Grounding Check | Pass/Fail |
|-----------|------------|------------------|---------------------------|----------------------|-------------------|------------------------|------------------|-----------|
| 3 | What is compound interest? | Numeric | Fidelity Compound Interest Page | | | Expected: Fidelity compound interest | | |
| 4 | How does a Roth 401(k) work? | Numeric | Fidelity Roth 401(k) Page | | | Expected: Fidelity Roth 401(k) | | |
| 5 | What is a traditional IRA? | Numeric | Fidelity Traditional IRA Page | | | Expected: Fidelity Traditional IRA | | |
| 6 | What is a rollover IRA? | Numeric | Fidelity Rollover IRA Page | | | Expected: Fidelity Rollover IRA | | |
| 7 | How does a 401(k) grow over time? | Numeric | Fidelity Compound Interest Page | | | Expected: Fidelity compound interest | | |
| 8 | What is the difference between a Roth IRA and traditional IRA? | Numeric | Both IRA Pages | | | Expected: Fidelity IRA sources | | |
| 9 | How much can I contribute to a 401(k)? | Numeric | Fidelity 401(k) Page | | | Expected: Fidelity 401(k) | | |
| 10 | What happens if I withdraw early from a Roth IRA? | Numeric | Fidelity Roth IRA Page | | | Expected: Fidelity Roth IRA | | |
| 12 | What is the penalty for withdrawing from a 401(k) early? | Numeric | Fidelity 401(k) Page | | | Expected: Fidelity 401(k) | | |
| 13 | How does compound interest affect retirement savings? | Numeric | Fidelity Compound Interest Page | | | Expected: Fidelity compound interest | | |
| 14 | What is a Roth conversion? | Numeric | Fidelity Roth IRA Page | | | Expected: Fidelity Roth IRA | | |
| 18 | What is the tax treatment of Roth IRA withdrawals? | Numeric | Fidelity Roth IRA Page | | | Expected: Fidelity Roth IRA | | |
| 19 | How do employer matches work in a 401(k)? | Numeric | Fidelity 401(k) Page | | | Expected: Fidelity 401(k) | | |
| 20 | What is the benefit of saving early for retirement? | Numeric | Fidelity Compound Interest Page | | | Expected: Fidelity compound interest | | |

---

# Evaluation Metrics

## Retrieval Accuracy
Measures whether the system retrieved the correct source document for each query.

## Citation Accuracy
Checks whether citations in the generated answer match the retrieved documents and avoid hallucinated sources.

## Grounding Pass Rate
Percentage of test cases where:
- The answer is grounded in retrieved documents
- No unsupported claims are introduced
- All statements trace back to expected sources

## Refusal Accuracy
Evaluates whether the system correctly refuses when:
- Required documents are missing
- The query cannot be answered using allowed sources

