## Retirement Readiness — Demo Script
### Purpose
This demo script shows how to set up, run, and test the Retirement Readiness application in a way that is easy to reproduce. The goal is for another person to follow these steps and get the same results.

### 1. Prerequisites
Make sure the following are installed:

- Python 3.10+
- Node.js 18+
- Git

### 2. Project Setup
- Clone the repository
- git clone <repository-url>
- cd Retirement-Readiness

### 3. Backend Setup
- Navigate to backend
    - cd backend
- Create virtual environment
    - python3 -m venv .venv
- Activate virtual environment
- Mac/Linux:
    - source .venv/bin/activate
- Windows:
    - .venv\Scripts\activate
- Install dependencies
    - pip install -r requirements.txt
- Create .env
- Create a file at backend/.env and add the following:
    - envGOOGLE_API_KEY=your_api_key_here

Important: Do not commit .env — it is ignored by .gitignore.

### 4. Start the Backend
- From the backend/ folder, run:
  - python3 -m uvicorn endpoint:app --reload

**Expected result:**
- The backend starts without errors
- The local API is available at: http://127.0.0.1:8000

Optional verification — open this in a browser:
http://127.0.0.1:8000/health 

Expected: a JSON response confirming the backend is running.

### 5. Frontend Setup
Open a new terminal and navigate to the frontend folder:
- cd frontend
- Install dependencies
    - npm install
- Start the frontend
    - npm run dev

**Expected result:**
- Vite starts successfully
- The app is available at: http://localhost:5173

### 6. Demo Flow
Follow the scenarios below in order.

### 7. Demo Scenario 1 — Basic Definition Question (Roth IRA)
**User Action**  
Click the button:
- What is a Roth IRA?

**Expected result:**
- The application generates a retirement‑related answer
- The answer includes a citation section
- The sources are clickable links
- The answer shows as Validated when grounded

**What to point out**
- The system can answer common retirement questions
- Answers include source grounding
- Users can verify information directly

### 8. Demo Scenario 2 — Basic Definition Question (401(k))
**User action**
Click the button:
- What is a 401(k)?

**Expected result**
- The system returns a clear explanation
- The answer includes citations when supported
- The UI displays source links

**What to point out**
- The application supports multiple retirement concepts
- Retrieval-based answering, not raw AI

### 9. Demo Scenario 3 — Basic Definition Question (Rollover IRA)
**User action**
Click the button:
- What is a Rollover IRA?

**Expected result**
- The system returns a grounded explanation
- Citations appear if supported by retrieved chunks

**What to point out**
- The app covers rollover‑specific retirement accounts
- Retrieval ensures accuracy across plan types

### 10. Demo Scenario 4 — Basic Definition Question (Traditional IRA)
**User action**
Click the button:
- What is a Traditional IRA?

**Expected result**
- The system returns a grounded explanation
- Citations appear if supported by retrieved chunks

**What to point out**
- This covers the second major IRA type
- Retrieval ensures accuracy and avoids hallucination

### 10. Demo Scenario 5 — Basic Definition Question (Roth 401k)
**User action**
Click the button:
- What is a Roth 401(k)?

**Expected result**
- The system returns a grounded explanation
- Citations appear if supported

**What to point out**
- The demo now covers all five required retirement topics
- Consistent UI behavior across all plan buttons

### 11. Demo Scenario 6 — Free-Text Question

**User action**
- Type the following into the text box and click Send:
  - **What is the difference between a Roth IRA and a Traditional IRA?**

**Expected result**
- The application generates a comparison answer
- If enough grounded source content exists, citations appear
- If not, the app falls back to general financial knowledge with a note

**What to point out**
- Users are not limited to the preset buttons
- The system supports fully custom questions
- The fallback system ensures a helpful answer is always returned

### 12. Demo Scenario 7 — Repair Loop Demonstration
**User action**
Type the following into the text box and click Send:
- **How much can I contribute to a Roth IRA this year if I’m 25 and make $90,000?**

**Expected result**
- The first-pass answer will include a specific contribution limit number (e.g., “$6,500”)
- That number does not appear in the retrieved source chunks, so:
- The numeric validator fails
- The grounding verifier may also flag unsupported phrases
- The system automatically triggers the repair loop
- The repaired answer removes unsupported numbers and aligns with retrieved sources
- The final answer passes validation and is returned to the UI

**What to point out**
- This scenario demonstrates the full validation pipeline
- The system detects:
    - Hallucinated numbers
    - Unsupported claims
    - Mismatched citations
The repair loop produces a clean, grounded, source‑aligned answer
This shows the project’s safety and reliability features working end‑to‑end


### 13. Demo Scenario 8 — Personalized Scenario Engine

**User action**
Open the Personalized Scenario and enter:  
- Age: 20
- Retirement Age: 65
- Annual Income: 70,000
- Current Savings: 2,000
- Monthly Contribution: 300  
Then click Run Scenario

### 10. Demo Scenario 4 — Personalized Scenario Engine

**User action**

Open the Personalized Scenario: Compound Interest section and enter:

| Field | Value |
|---|---:|
|Age | 20 |
|Retirement Age | 65 |
|Annual Income | 70,000 |
|Current Savings | 2,000 |
|Monthly Contribution | 300 |

Then click Run Scenario.

**Expected result**
- The app calculates a projected retirement balance
- The result includes a short plain-English explanation
- The response appears in the same styled answer area as other answers

**What to point out**
- This is not just a Q&A bot — it includes a personalized projection workflow
- The backend combines compound interest calculation logic with source-based educational context

### Mathmatical Verification

To verify that the projection is mathmatically correct, we teseted a scenario using the same inputs and formula. We used excel sheets, outside of the system.

Test scenario used for verifcation:
- Age: 25
- Retirement Age: 65
- Annual Income: $60,000  
- Current Savings: $1  
- Monthly Contribution: $500  
- Return Rate: 3.5% (default in system) 

Using the standard compund intreset formula with monthly contributions:

Future Value = P(1 + r/12)^(12t) + PMT * [((1 + r/12)^(12t) − 1) / (r/12)]

Where:
- P = current savings  
- PMT = monthly contribution  
- r = annual return rate  
- t = years  

We verified this calculation in Execl uaing the same formula as the backend. This formula combines the growth of current savings and the growth of monthly contributions:

=ROUND((1*(1+3.5%/12)^(40*12)) + (500*(((1+3.5%/12)^(40*12)-1)/(3.5%/12))),2)

Expected result: $522,337.49

This matches the output generated by the application, confirming that the projects logic is correct.

### 14. Demo Scenario 9 — Source Verification

**User action**
Under any generated answer, click one of the source links.

**Expected result**
- The source opens in a new browser tab
- The user can inspect the referenced material directly

**What to point out**
- The project supports full transparency
- Users can verify exactly where the information came from
- This reduces black-box AI behavior and builds trust

### 15. Demo Scenario 10 — Fallback Behavior

**User action**
Type the following into the text box and click Send:
- **How should I think about retirement planning when I am just starting my career?**

**Expected result**
- The system still returns a helpful answer
- The response may indicate it is based on general financial knowledge rather than directly grounded project sources
- The application does not fail or return an empty response

**What to point out**
- The fallback system prevents dead ends
- The app remains useful even when exact source retrieval is weak