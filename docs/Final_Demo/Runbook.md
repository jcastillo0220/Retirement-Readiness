# Final Demo Runbook

This runbook describes how to set up, run, and operate the **Retirement Readiness** application for demos, testing, and development. It covers environment preparation, backend and frontend startup, cache behavior, scenario engine usage, and debugging workflows.

---

# 1. Prerequisites

## Backend Requirements
- Python 3.10+
- pip (Python package manager)
- Uvicorn
- FastAPI
- python‑dotenv
- BeautifulSoup4
- Requests
- PyPDF2
- google‑genai (Gemini API)

## Frontend Requirements
- Node.js 18+
- npm
- Vite
- TailwindCSS + PostCSS
- rehype‑raw

## System Requirements
- VS Code recommended
- Internet connection (Gemini API + external source fetching)
- Ability to run two terminals simultaneously (backend + frontend)

---

# 2. Environment Setup

## 2.1 Backend Setup
From the project root:
```bash
cd backend
```
Verify Python:
```bash
py --version
```

Verify pip:
```bash
py -m pip --version
```

Install required packages:
```bash
py -m pip install uvicorn fastapi python-dotenv beautifulsoup4 requests PyPDF2 google-genai
```

## 2.2 Environment Variables
Create a `.env` file inside `/backend`
```bash
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-number-model
```
Ensure `.env` is **never committed** to GitHub

# 3. Starting the Backend
From `/backend`:
```bash
py -m uvicorn endpoint:app --reload
```
If successful, you should see:
```bash
Uvicorn running on http://127.0.0.1:8000
```
Keep this terminal open and running

# 4. Starting the Frontend
Open a second terminal:
```bash
cd frontend
```

Verify Node:
```bash
node --version
```

Install dependencies:
```bash
npm install
```

Install Vite:
```bash
npm install -g vite
```

Install Tailwind + PostCSS:
```bash
npm install -D tailwindcss postcss autoprefixer
```

Install rehype‑raw:
```bash
npm install rehype-raw
```

Run the dev server:
```bash
npm run dev
```

Navigate to the printed localhost URL (usually `http://127.0.0.1:5173`).

# 5. System Architecture Overview
The system consists of:
- Frontend (React + Vite)
    - Sends user questions and scenario inputs to the backend.
- Backend (FastAPI)
    - Loads and chunks PDF/web sources
    - Runs Gemini for answer generation
    - Validates answers
    - Repairs incorrect answers
    - Caches validated answers
    - Serves scenario projections
- In‑Memory Cache
    - Stores validated answers keyed by question text.
- Chunk Loader
    - Rebuilds source chunks on backend restart or source change.

# 6. Cache Invalidation Workflow
The backend uses an in‑memory cache, which resets automatically when:

## Cache is cleared when:
- Backend restarts
- Source files change (PDF replaced, URL changed, etc.)
- Chunk loader re-runs
- Chunking logic changes

## Demo Example: 401(k) Source Change
1. Ask:
    **“What is a 401(k)?”**
    → Cached answer is generated from Northwestern Mutual PDF.
2. Change the source to:
    **Fidelity — What Is a 401(k)?**
3. Restart backend → cache clears → chunks reload.
4. Ask again:
    **“What is a 401(k)?”**
    → New answer is generated from Fidelity.

# 7. Using the Scenario Engine
The scenario engine lives at:
```bash
POST /api/scenario
```

## Inputs
The frontend sends a JSON payload like:
```bash
{
    "age": 30,
    "retirment_age": 65,
    "annual_income": 65000,
    "current_savings": 15000,
    "monthly_contribution": 400,
    "assumed_return_rate": return_rate,
    "projected_balance": future_value,
}
```
## Outputs
The backend returns:
- A retirement projection
- A narrative explanation
- Key assumptions
- Contribution recommendations

## How to Demo
1. Open the frontend.
2. Enter a realistic scenario.
3. Submit.
4. Show:
    - The projection graph
    - The explanation text
    - The assumptions section

# 8. Using the Repair Loop
The repair loop ensures that every answer returned to the user is grounded, cited, and validated. It activates automatically whenever the validator detects issues in the model’s initial response.
---

The repair loop is triggered when:
- Missing citations
- Citations that do not match retrieved source chunks
- Claims that contradict source material
- Unsupported numeric claims
- Incomplete, vague, or overly general explanations
- Malformed validation JSON
- Inline links or hallucinated sources
- Any validator‑flagged factual inconsistencie


## Repair Loop Steps
1. Gemini generates an initial answer
The backend sends a structured prompt containing:
- The user’s question
- The retrieved source chunks
- Instructions to cite and ground the answer
2. The validator checks the answer
The validator inspects:
- Citation format (must start with “According to…”)
- Citation grounding (must map to real chunks)
- Numeric grounding (numbers must appear in source text)
- Source consistency (no contradictions)
- Validation JSON (if present)
3. If validation fails → the repair loop activates
The system does not return the answer.
Instead, it builds a repair prompt containing:
- The user’s question
- The flawed answer
- A list of validator errors
- The source context
4. Gemini rewrites the answer
The model is explicitly instructed to:
- Fix the errors
- Use only the provided sources
- Avoid hallucinations
- Produce a grounded, citation‑correct answer
5. The repaired answer is validated again
The validator re-runs the full grounding checks.
6. If the answer passes validation
- It is cached
- It is returned to the user
- The original (failed) answer is discarded

## Repair Loop Failure Modes
The repair loop attempts up to 3 times

The repair loop fails when:
1. The model repeatedly contradicts the sources
Example:
Gemini insists that a Roth IRA has employer matching (it does not).
2. The model refuses to cite or produces invalid citation format
Example:
- Missing “According to…”
- Missing Markdown link
- Citing a source not in retrieved chunks
3. The model invents unsupported numbers
Example:
- Contribution limits not found in the source
- Withdrawal penalties not present in the chunk set
4. The model produces irrelevant or empty text
Example:
- Generic financial advice
- No answer body
- Only disclaimers
5. The model returns malformed or unusable validation JSON
Example:
- JSON missing required fields
- JSON embedded inside Markdown code blocks
6. The model refuses to answer due to safety misunderstandings
Example:
- Treats retirement questions as “financial advice” and refuses

# 9. Common Errors & Fixes

## Backend won’t start
Cause: Missing dependencies

Fix:
Install manually all of the requirements listed above

## Gemini API key not found
Cause: .env missing or misnamed

Fix:
Ensure file is named .env and contains:
```bash
GEMINI_API_KEY=your_key
```
Restart backend.

## CORS errors in frontend
Cause: Frontend cannot reach backend

Fix:
Ensure backend is running at `http://127.0.0.1:8000`
Check `vite.config.js` proxy settings if used.

## Scenario engine returns null values
Cause: Missing or malformed JSON

Fix:
Ensure all required fields are provided.

## Answers not updating after source change
Cause: Backend not restarted

Fix:
Stop backend → restart → chunks reload → cache clears.

## PDF not loading
Cause: File path incorrect or PDF corrupted

Fix:
Verify path in the chunk loader.

## 10. Final Demo Checklist
Before the demo
- Backend running
- Frontend running
- .env loaded
- Sources loaded
- Internet connection stable
During the demo
- Show scenario engine
- Show repair loop
- Show cache invalidation
- Show citations and grounding
- Show UI flow
After the demo
- Stop backend
- Stop frontend
