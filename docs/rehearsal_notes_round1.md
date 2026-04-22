# End-to-End Demo Rehearsal Round 1

## Demo Scenario 1 — Basic Definition Question (Roth IRA)
- Answer produced in <5 seconds
- Grounding 100%

## Demo Scenario 2 — Basic Definition Question (401(k))
- Answer produced in <5 seconds
- Answer a little vauge: A 401(k) is a type of employer-sponsored retirement plan. It is considered a qualified plan. Some 401(k)s can also be established as a Designated Roth Account.
- Grounding 100% but missing most of the answer

## Demo Scenario 3 — Basic Definition Question (Rollover IRA)
- Answer produced in <5 seconds
- Grounding 100% missing again some of the answer


## Demo Scenario 4 — Basic Definition Question (Traditional IRA)
- Answer produced in <5 seconds
- Grounding 80%

## Demo Scenario 5 — Basic Definition Question (Roth 401k)
- Refusal to answer: The provided source excerpts do not contain a definition of a Roth 401(k). The text primarily consists of navigation menus and general information about Fidelity's website sections.

## Demo Scenario 6 — Free-Text Question
- Answer produced in <7 seconds
- Grounding 75%

## Demo Scenario 7 — Repair Loop Demonstration
- Answer produced in <15 seconds
- Grounding 50%
- Good answer provided: For 2024, you can contribute up to $7,000 to a Roth IRA. This amount cannot exceed 100% of your compensation and depends on your modified adjusted gross income being within specific limits. An additional $1,000 catch-up contribution is available for individuals age 50 and over.
- Validated pill is broken, should be corrected

## Demo Scenario 8 — Out-of-Scope Refusal (Live)
- Refuses correctly

## Demo Scenario 9 — Personalized Scenario Engine
- Answer produced in <15 seconds
- Explanation outputs variable from code retirement_age isntead of 'retirement age'
- Grounding report includes redundant phrases such as: Your current yearly income: Not supported
estimated balance at retirement: Not supported

## Demo Scenario 10 — Source Verification
- Link takes me to the correct source document 

## Demo Scenario 11 — Fallback Behavior
- Grounded answer that does not give out any finanical advice but points to education
- ANSWER: When starting your career, you can begin by exploring various retirement accounts. For example, Roth IRAs allow you to save and invest money you've already paid taxes on, with the opportunity for tax-free withdrawals in retirement. Fidelity offers resources on retirement planning, retirement accounts, and retirement education to help you learn more.