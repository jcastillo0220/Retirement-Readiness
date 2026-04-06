# Retirement Readiness Evaluation Starter Kit

| # | User Query | Expected Source Document | Retrieved Documents | Generated Answer | Grounding Accuracy | Refusal Accuracy |
|---|------------|---------------------------|----------------------|-------------------|------------------|------------------|
| 1 | What is a Roth IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A Roth IRA allows eligible individuals to make contributions that are not tax-deductible. The main benefit is that qualified distributions from a Roth IRA are received income-tax-free, provided certain conditions are met, such as the account being open for at least five years. | Pass | 
| 2 | How do taxesd work in a Roth IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF |You contribute money to a Roth IRA after you've already paid taxes on it. Your investments can grow tax-free, and when you make qualified withdrawals in retirement, they are also completely tax-free. | Pass | 
| 3 | What are qualified withdrawals? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | I could not find a verified source for that question, so I can’t provide a grounded answer right now. | Fail | 
| 4 | What are contribution limits? | Expected Northwestern Mutual PDF | Northwestern Mutual PDF | AThe Roth IRA contribution limit is typically set annually by the IRS. For 2024, you can contribute up to $7,000. If you are age 50 or older, you may contribute an additional $1,000, bringing your total to $8,000. | Pass |
| 5 | Roth vs Traditional IRA | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A Traditional IRA allows for potentially tax-deductible contributions, meaning withdrawals in retirement will be taxed. In contrast, contributions to a Roth IRA are made with after-tax money, and qualified withdrawals are entirely tax-free. | Pass |
| 6 | What is a 401(k)? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A 401(k) is a popular employer-sponsored retirement savings plan that allows employees to contribute a portion of their paycheck before taxes are taken out. Your contributions and investment earnings grow tax-deferred until retirement, and employers often offer matching contributions. | Pass |
| 7 | How does a 401(k) work? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A 401(k) is an employer-sponsored retirement savings plan that lets you invest a portion of each paycheck. This plan comes with special tax benefits, often allowing contributions before taxes are deducted. | Pass |
| 8 | What are 401(k) tax rules? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | Most 401(k) contributions are made before taxes are deducted, which can lower your taxable income today. When you take withdrawals in retirement, these funds from pre-tax contributions are then typically taxed as ordinary income. | Pass |
| 9 | What is a Traditional IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A Traditional IRA is a basic individual retirement account that allows for deductible and non-deductible contributions. Your investments in a Traditional IRA grow tax-deferred, meaning you don't pay taxes until you make withdrawals in retirement. | Pass |
| 10 | How are Traditional IRAs taxed? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | I could not find a verified source for that question, so I can’t provide a grounded answer right now. | Fail |
| 11 | Traditional IRA contribution rules | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | To contribute to a Traditional IRA, you must have earned income. There are annual limits on how much you can contribute, and those aged 50 and over may be able to contribute an additional catch-up amount. There is no age limit to contribute as long as you have earned income. | Pass |
| 12 | What is a Rollover IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | I could not find a verified source for that question, so I can’t provide a grounded answer right now. | Fail |
| 13 | How do taxes work in a Rollover IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A Rollover IRA allows your money to grow tax-deferred, meaning you won't pay taxes on its potential growth until you make withdrawals. The initial transfer of funds from a workplace account into a Rollover IRA is generally done without taxes or penalties. However, when you eventually withdraw money, it will be subject to state and federal income taxes, and withdrawals before age 59½ may also incur a 10% early withdrawal penalty. | Pass |
| 14 | When to use a Rollover IRA? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A Rollover IRA is typically used when you leave a job or retire. It allows you to move funds from your old workplace retirement plan into a single account, often without immediate taxes or penalties. | Pass |
| 15 | What is a Roth 401(k)? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A Roth 401(k) is an employer-sponsored retirement plan, also known as a Designated Roth Account, that allows you to contribute money after taxes. While contributions are not tax-deductible, your qualified withdrawals in retirement are entirely tax-free. | Pass |
| 16 | Roth 401(k) vs Roth IRA | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | A Roth 401(k) is an employer-sponsored retirement plan, while a Roth IRA is an individual retirement account you open on your own. Roth 401(k)s generally have higher contribution limits and no income phase-outs for contributions, which can apply to Roth IRAs. | Pass |
| 17 | How do taxes work in a Roth 401(k)? | Expected: Northwestern Mutual PDF | Northwestern Mutual PDF | With a Roth 401(k), you contribute money after it has already been taxed from your paycheck. This allows your investments to grow completely tax-free, and qualified withdrawals in retirement are also tax-free. | Pass |


# Scenario Test Cases

| # | Scenario | Expected Source Document | Retrieved Documents | Expected Numerical Outputs | Numerical Outputs | Generated Answer | Grounding Accuracy  | Refusal Accuracy |
|---|------------|---------------------------|----------------------|----------------------|----------------------|-------------------|------------------|------------------|
| 18 | Scenario | Expected: Fidelity | Fidelity - Compound Interest | age: 20, retirement age: 70, years to grow: 50, annual income: 75000, current savings: 10000, monthly contribution: 500, assumed return rate: 0.035, projected balance: 841265.01 | age: 20, retirement age: 70, years to grow: 50, annual income: 75000, current savings: 10000, monthly contribution: 500, assumed return rate: 0.035, projected balance: 841265.01 |  Explanation of Projection With 23 years until your planned retirement, your current savings and future monthly contributions are projected to grow to approximately $160,444.83. This estimate is based on an assumed 3.5% annual return, which is compounded monthly. This illustrates how compound interest allows your money to grow over time. Explanation of Inputs Age: Your current age, which helps determine the duration of your investment period. Retirement Age: The age at which you plan to retire and begin using your savings.Years to grow: This refers to the 23 years remaining for your investments to grow before retirement. Income: Your current earnings, influencing how much you can contribute to savings. Current Savings: The existing amount of money you have accumulated in your retirement accounts. Monthly Contribution: The regular sum you plan to add to your savings each month. Return Rate: This is the 3.5% annual rate your investments are expected to earn, compounded monthly, significantly impacting your total growth. | Pass |
| 19 | Scenario | Expected: Fidelity | Fidelity - Compound Interest | age: 42, retirement age: 65, years to grow: 23, annual income: 65000, current savings: 15000, monthly contribution: 300, assumed return rate: 0.035, projected balance: 160444.83 | age: 42, retirement age: 65, years to grow: 23, annual income: 65000, current savings: 15000, monthly contribution: 300, assumed return rate: 0.035, projected balance: 160444.83 |  Explanation of Projection This projection indicates that with 50 years until retirement, your combined savings and monthly contributions could reach approximately $841,265.01. This potential growth is based on an assumed 3.5% annual return, which is compounded monthly, highlighting the benefit of long-term investment. Explanation of Inputs Age: This represents your current age, which helps determine the duration of your savings journey.Retirement Age: This is the age you anticipate retiring, marking the goal for your investment period. Years to grow: This is the 50-year period during which your investments will accumulate value. Income: This represents your current earnings, a factor in how much you can contribute to savings. Current Savings: This is the initial amount you have already accumulated towards your retirement. Monthly Contribution: This is the regular amount you plan to add to your savings each month. Return Rate: This is the assumed 3.5% annual rate at which your investments are expected to grow. | Pass |
| 20 | Scenario | Expected: Fidelity | Fidelity - Compound Interest | age: 50, retirement age: 68, years to grow: 18, annual income: 80000, current savings: 105000, monthly contribution: 1200, assumed return rate: 0.035, projected balance: 557334.45 | age: 50, retirement age: 68, years to grow: 18, annual income: 80000, current savings: 105000, monthly contribution: 1200, assumed return rate: 0.035, projected balance: 557334.45 | Explanation of Projection This projection estimates that your retirement savings could grow to approximately $557,334.45 over the next 18 years. This growth is based on a 3.5% annual return, compounded monthly, illustrating how compound interest can help build wealth over time. Explanation of Inputs Age: Your current age is 50, which helps determine the remaining time for your savings to grow. Retirement age: You plan to retire at age 65, marking the end of your accumulation period. Years to grow: You have 18 years for your investments to compound and increase in value. Income: Your current annual income is $70,000, which supports your ability to save. Current savings: You currently have $105,000 saved, which forms the starting capital for your retirement fund. Monthly contribution: You are contributing $1,200 each month to your retirement account. Return rate: Your investments are expected to yield a 3.5% annual return, compounded monthly. | Pass |

# Required Metrics

| Retriveal Accuracy | Citation Coverage | Grounding Accuracy | Halluication Rate | Refusal Accuracy |
|--------------------|-------------------|---------------------|------------------|---------------------|
| 100% | 100% | 85% | 5% | 100% |

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
