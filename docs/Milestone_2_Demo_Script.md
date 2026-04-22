## Retirement Readiness — Demo Script

### Purpose
This demo script shows how to set up, run, and test the Retirement Readiness application in a way that is easy to reproduce. The goal is for another person to follow these steps and get the same results.

---

### 1. Prerequisites
Make sure the following are installed:

- Python 3.10+
- Node.js 18+
- Git

---

### 2. Project Setup
- Clone the repository  
- git clone <repository-url>  
- cd Retirement-Readiness  

---

### 3. Backend Setup
- Navigate to backend  
  - cd backend  
- Create virtual environment  
  - python3 -m venv .venv  
- Activate virtual environment  
  - Mac/Linux: source .venv/bin/activate  
  - Windows: .venv\Scripts\activate  
- Install dependencies  
  - pip install -r requirements.txt  

- Create .env  
- Create a file at backend/.env and add:
  GOOGLE_API_KEY=your_api_key_here

Important: Do not commit .env — it is ignored by .gitignore.

---

### 4. Start the Backend
From the backend/ folder, run:

python3 -m uvicorn endpoint:app --reload

Expected result:
- Backend starts without errors  
- API available at: http://127.0.0.1:8000  

Optional:
http://127.0.0.1:8000/health  

---

### 5. Frontend Setup
Open a new terminal:

cd frontend  
npm install  
npm run dev  

Expected result:
- App runs at: http://localhost:5173  

---

## 6. Demo Flow

---

### 7. Demo Scenario 1 — Roth IRA
User Action:
Click: What is a Roth IRA?

Expected:
- Grounded answer
- Citations shown
- Validated badge appears

---

### 8. Demo Scenario 2 — 401(k)
User Action:
Click: What is a 401(k)?

Expected:
- Clear explanation
- Citations displayed

---

### 9. Demo Scenario 3 — Rollover IRA
User Action:
Click: What is a Rollover IRA?

Expected:
- Grounded explanation
- Citations shown

---

### 10. Demo Scenario 4 — Traditional IRA
User Action:
Click: What is a Traditional IRA?

Expected:
- Grounded explanation
- Citations shown

---

### 11. Demo Scenario 5 — Roth 401(k)
User Action:
Click: What is a Roth 401(k)?

Expected:
- Grounded explanation
- Citations shown

---

### 12. Demo Scenario 6 — Free-Text Question
User Action:
Type and send:
What is the difference between a Roth IRA and a Traditional IRA?

Expected:
- Comparison answer
- May include citations
- Shows system handles custom input

---

### 13. Demo Scenario 7 — Out-of-Scope Refusal (Live)
User Action:
Type and send:
What is the best recipe for banana bread?

Expected:
- System refuses to answer
- Displays out-of-scope message

Example Output:
This assistant only covers retirement account topics such as IRAs, 401(k) plans, and compound interest. Your question appears to be outside that scope. Please ask a retirement-related question and I'll be happy to help.

What to point out:
- No hallucination
- No citations
- Clear scope enforcement

---

### 14. Demo Scenario 8 — Repair Loop Demonstration
User Action:
Type and send:
How much can I contribute to a Roth IRA this year?

Expected:
- Initial answer may contain unsupported number
- Validation fails
- Repair loop triggers
- Final answer is corrected and validated

---

### 15. Demo Scenario 9 — Personalized Scenario Engine
User Action:
Enter:

Age: 20  
Retirement Age: 65  
Annual Income: 70000  
Current Savings: 2000  
Monthly Contribution: 300  

Click Run Scenario

Expected:
- Returns projected balance
- Shows explanation

---

### Mathematical Verification

Future Value Formula:

Future Value = P(1 + r/12)^(12t) + PMT * [((1 + r/12)^(12t) − 1) / (r/12)]

Excel Verification:

=ROUND((1*(1+3.5%/12)^(40*12)) + (500*(((1+3.5%/12)^(40*12)-1)/(3.5%/12))),2)

Expected Output:
$522,337.49

---

### 16. Demo Scenario 10 — Source Verification
User Action:
Click any source link

Expected:
- Opens source in browser
- Confirms transparency

---

### 17. Demo Scenario 11 — Fallback Behavior
User Action:
Type and send:
How should I think about retirement planning?

Expected:
- System returns helpful answer
- May use general knowledge
- No failure