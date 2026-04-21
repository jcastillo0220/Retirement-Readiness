# Retirement Readiness Evaluation Starter Kit

| # | User Query | Expected Source Document | Retrieved Documents | Generated Answer | Refusal Accuracy | Grounding Accuracy |
|---|------------|---------------------------|----------------------|-------------------|------------------|------------------|
| 1 | What is a Roth IRA? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS — Roth Ira | A Roth IRA is an individual retirement account where contributions are not tax-deductible. For eligible individuals, distributions from a Roth IRA are received income-tax-free, provided at least five years have passed since the first contribution and certain conditions are met. Eligibility and maximum contribution amounts depend on an individual's modified adjusted gross income and compensation. | Pass | 100%
| 2 | How do taxes work in a Roth IRA? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS — Roth Ira | A Roth IRA allows you to save and invest money on which you have already paid taxes. This means that when you make withdrawals in retirement, they have the opportunity to be tax-free. | Pass | 100%
| 3 | What are qualified withdrawals? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS — Roth Ira | Qualified withdrawals from a Roth IRA are those that offer the opportunity to make tax-free withdrawals in retirement. | Pass | 87.5%
| 4 | What are contribution limits? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS — Roth Ira | A Roth IRA allows you to save and invest money on which you've already paid taxes. Unlike traditional IRAs, Roth IRAs have income limits that may exclude some savers from contributing. High earners, however, still have a couple of options. | Pass | 100%
| 5 | Roth vs Traditional IRA | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS — Roth Ira | A Traditional IRA offers deductible or non-deductible contributions and provides tax-deferred growth. In contrast, a Roth IRA involves non-deductible contributions. Distributions from a Roth IRA are received income-tax-free, provided at least five years have passed since the first contribution and certain conditions are met. | Pass | 92.9%
| 6 | What is a 401(k)? | Expected: Fidelity & IRS | Fidelity - 401k & IRS - 401k |A 401(k) is an employer-sponsored retirement plan. It is classified as a qualified plan. These plans can be set up as pre-tax accounts or as a Designated Roth Account. | Pass | 100%
| 7 | How does a 401(k) work? | Expected: Fidelity & IRS | Fidelity - 401k & IRS - 401k | A 401(k) is a popular retirement savings plan offered through a workplace. It allows you to invest a portion of each paycheck, often before taxes are deducted, depending on the type of contributions made. Because of its tax advantages, the federal government places some restrictions on when you can withdraw your contributions. | Pass | 73%
| 8 | What are 401(k) tax rules? | Expected: Fidelity & IRS | Fidelity - 401k & IRS - 401k | A 401(k) is a retirement savings plan that allows you to invest a portion of your paycheck. Depending on the contribution type, these funds can be invested before taxes are deducted. The federal government imposes restrictions on when you can withdraw your 401(k) contributions due to their tax advantages. | Pass | 60%
| 9 | What is a Traditional IRA? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS - Tradtional Ira | A Traditional IRA is the most basic type of Individual Retirement Arrangement available. It offers both deductible and non-deductible contributions, and the investments within it grow tax-deferred. | Pass | 100%
| 10 | How are Traditional IRAs taxed? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS - Tradtional | Traditional IRA contributions may be tax-deductible, depending on your income and other retirement plan participation. The money in the account grows tax-deferred, meaning taxes are typically paid when you withdraw the funds in retirement. | Pass | 75%
| 11 | Traditional IRA contribution rules | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS - Tradtional | Traditional IRAs allow for both deductible and non-deductible contributions. Your ability to deduct contributions depends on your tax-filing status, modified adjusted gross income, and participation in an employer-sponsored retirement plan. | Pass | 60%
| 12 | What is a Rollover IRA? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS - Rollover Ira | A Traditional Rollover IRA is identified as a type of individual retirement plan. It is associated with the concept of rollovers, which involve moving retirement plan and IRA distributions between different plans. | Pass | 33%
| 13 | How do taxes work in a Rollover IRA? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS - Rollover Ira | A Rollover IRA typically allows your investments to grow without immediate taxation, meaning growth is tax-deferred. However, when funds are transferred, some amounts might need to be included in your income if they are not rolled over according to specific rules. | Pass | 25%
| 14 | When to use a Rollover IRA? | Expected: Northwestern Mutual PDF & IRS | Northwestern Mutual PDF & IRS - Rollover Ira | A Rollover IRA is an individual retirement plan designed to receive funds from other retirement accounts. People typically use it when moving money from an employer-sponsored plan, such as a 401(k) or 403(b), into their own individual retirement arrangement. | Pass | 50%
| 15 | What is a Roth 401(k)? | Expected: Fidelity & IRS | Fidelity - Roth 401k & IRS - Roth 401k | A Roth 401(k) is an employer-sponsored retirement plan, also known as a Designated Roth Account, that allows you to contribute money after taxes. While contributions are not tax-deductible, your qualified withdrawals in retirement are entirely tax-free. | Pass | 16.6%
| 16 | Roth 401(k) vs Roth IRA | Expected: Fidelity & IRS | Fidelity - Roth 401k & IRS - Roth 401kF | A Roth 401(k) is an employer-sponsored retirement plan, while a Roth IRA is an individual retirement account you open on your own. Roth 401(k)s generally have higher contribution limits and no income phase-outs for contributions, which can apply to Roth IRAs. | Pass | 100%
| 17 | How do taxes work in a Roth 401(k)? | Expected: Fidelity & IRS | Fidelity - Roth 401k & IRS - Roth 401k | With a Roth 401(k), you contribute money after it has already been taxed from your paycheck. This allows your investments to grow completely tax-free, and qualified withdrawals in retirement are also tax-free. | Pass | 0% |


# Scenario Test Cases

| # | Scenario | Expected Source Document | Retrieved Documents | Expected Numerical Outputs | Numerical Outputs | Generated Answer | Grounding Accuracy  | Refusal Accuracy |
|---|------------|---------------------------|----------------------|----------------------|----------------------|-------------------|------------------|------------------|
| S-1 | Scenario | Expected: Fidelity | Fidelity - Compound Interest | age: 20, retirement age: 70, years to grow: 50, annual income: 75000, current savings: 10000, monthly contribution: 500, assumed return rate: 0.035, projected balance: 841265.01 | age: 20, retirement age: 70, years to grow: 50, annual income: 75000, current savings: 10000, monthly contribution: 500, assumed return rate: 0.035, projected balance: 841265.01 |  Explanation of Projection With 23 years until your planned retirement, your current savings and future monthly contributions are projected to grow to approximately $160,444.83. This estimate is based on an assumed 3.5% annual return, which is compounded monthly. This illustrates how compound interest allows your money to grow over time. Explanation of Inputs Age: Your current age, which helps determine the duration of your investment period. Retirement Age: The age at which you plan to retire and begin using your savings.Years to grow: This refers to the 23 years remaining for your investments to grow before retirement. Income: Your current earnings, influencing how much you can contribute to savings. Current Savings: The existing amount of money you have accumulated in your retirement accounts. Monthly Contribution: The regular sum you plan to add to your savings each month. Return Rate: This is the 3.5% annual rate your investments are expected to earn, compounded monthly, significantly impacting your total growth. | N/A | 100% |
| S-2 | Scenario | Expected: Fidelity | Fidelity - Compound Interest | age: 42, retirement age: 65, years to grow: 23, annual income: 65000, current savings: 15000, monthly contribution: 300, assumed return rate: 0.035, projected balance: 160444.83 | age: 42, retirement age: 65, years to grow: 23, annual income: 65000, current savings: 15000, monthly contribution: 300, assumed return rate: 0.035, projected balance: 160444.83 |  Explanation of Projection This projection indicates that with 50 years until retirement, your combined savings and monthly contributions could reach approximately $841,265.01. This potential growth is based on an assumed 3.5% annual return, which is compounded monthly, highlighting the benefit of long-term investment. Explanation of Inputs Age: This represents your current age, which helps determine the duration of your savings journey.Retirement Age: This is the age you anticipate retiring, marking the goal for your investment period. Years to grow: This is the 50-year period during which your investments will accumulate value. Income: This represents your current earnings, a factor in how much you can contribute to savings. Current Savings: This is the initial amount you have already accumulated towards your retirement. Monthly Contribution: This is the regular amount you plan to add to your savings each month. Return Rate: This is the assumed 3.5% annual rate at which your investments are expected to grow. | N/A | 100% |
| S-3 | Scenario | Expected: Fidelity | Fidelity - Compound Interest | age: 50, retirement age: 68, years to grow: 18, annual income: 80000, current savings: 105000, monthly contribution: 1200, assumed return rate: 0.035, projected balance: 557334.45 | age: 50, retirement age: 68, years to grow: 18, annual income: 80000, current savings: 105000, monthly contribution: 1200, assumed return rate: 0.035, projected balance: 557334.45 | Explanation of Projection This projection estimates that your retirement savings could grow to approximately $557,334.45 over the next 18 years. This growth is based on a 3.5% annual return, compounded monthly, illustrating how compound interest can help build wealth over time. Explanation of Inputs Age: Your current age is 50, which helps determine the remaining time for your savings to grow. Retirement age: You plan to retire at age 65, marking the end of your accumulation period. Years to grow: You have 18 years for your investments to compound and increase in value. Income: Your current annual income is $70,000, which supports your ability to save. Current savings: You currently have $105,000 saved, which forms the starting capital for your retirement fund. Monthly contribution: You are contributing $1,200 each month to your retirement account. Return rate: Your investments are expected to yield a 3.5% annual return, compounded monthly. | N/A | 100% |

# Refusal Test Cases

The system should refuse or clearly disclaim answers for queries that are out of scope, unrelated to retirement, or have no supporting source content. In all refusal cases the expected behavior is the same: the system should **not** fabricate a grounded answer, should **not** cite a source it did not use, and should return either a clear disclaimer or a polite out-of-scope message.

| # | User Query | Query Type | Expected Behavior | Expected Source | Citation Expected | Grounding Check | Pass Condition |
|---|------------|------------|-------------------|-----------------|-------------------|-----------------|----------------|
| R-01 | What stocks should I buy right now? | Out-of-scope — investment advice | System returns a disclaimer stating it only covers retirement account education, not live investment recommendations. No source is cited. | None | No | N/A — refusal expected | Pass if no source is cited and a clear scope disclaimer is returned |
| R-02 | What is the best recipe for banana bread? | Non-retirement question | System returns a polite message that the question is outside the scope of the retirement assistant. No answer is generated. | None | No | N/A — refusal expected | Pass if the system does not attempt to answer and returns an out-of-scope message |
| R-03 | What will the stock market do next year? | No supporting source — speculative financial query | System returns a general knowledge disclaimer noting that no project sources support a forward-looking market prediction, and declines to speculate. No source is cited. | None | No | N/A — refusal expected | Pass if the answer contains a disclaimer and does not cite any loaded source |

# Grounding Failure Analysis (<70%)
| Test Case | Grounding Accuracy | Explaination | 
|-----------|--------------------|--------------|
| 3 | 47% | Phrase chunking was too agressive and answer included redundant calls to its source.

# Required Metrics

| Retrieval Accuracy | Citation Coverage | Grounding Accuracy | Halluication Rate | Refusal Accuracy |
|--------------------|-------------------|---------------------|------------------|---------------------|
| 94% | 100% | 48.3% | 15% | 100% |

# Metrics Explanation 
**Retrieval Accuracy**
Measures whether the system pulled the correct source chunks for the query.
- Formula:
Correctly retrieved chunks ÷ Total test cases

**Citation Coverage**
Tracks how often the model includes at least one citation marker in its answer.
- Formula:
Answers containing citation markers ÷ Total answers

**Grounding Accuracy**
Checks whether key phrases in the answer are supported by the retrieved chunks.
- Formula:
Supported key phrases ÷ Total key phrases evaluated

**Hallucination Rate**
Measures how often the model introduces claims not found in the retrieved source data.
- Formula:
Answers with unsupported claims ÷ Total answers

**Refusal Accuracy**
Evaluates whether the system correctly refuses queries that have no relevant or valid source support.
- Formula:
Correct refusals ÷ Total cases requiring refusal