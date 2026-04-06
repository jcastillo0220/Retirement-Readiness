Retirement Readiness — Demo Script
Purpose
This demo script shows how to set up, run, and test the Retirement Readiness application in a way that is easy to reproduce.
The goal is for another person to follow these steps and get the same results.

1. Prerequisites
Make sure the following are installed:

Python 3.10+
Node.js 18+
Git


2. Project Setup
Clone the repository
bashgit clone <repository-url>
cd Retirement-Readiness

3. Backend Setup
Navigate to backend
bashcd backend
Create virtual environment
bashpython3 -m venv .venv
Activate virtual environment
Mac/Linux:
bashsource .venv/bin/activate
Windows:
bash.venv\Scripts\activate
Install dependencies
bashpip install -r requirements.txt
Create .env
Create a file at backend/.env and add the following:
envGOOGLE_API_KEY=your_api_key_here

Important: Do not commit .env — it is ignored by .gitignore.


4. Start the Backend
From the backend/ folder, run:
bash python3 -m uvicorn endpoint:app --reload
Expected result:

The backend starts without errors
The local API is available at: http://127.0.0.1:8000

Optional verification — open this in a browser:
http://127.0.0.1:8000/health
Expected: a JSON response confirming the backend is running.

5. Frontend Setup
Open a new terminal and navigate to the frontend folder:
bashcd frontend
Install dependencies
bashnpm install
Start the frontend
bashnpm run dev
Expected result:

Vite starts successfully
The app is available at: http://localhost:5173


6. Demo Flow
Follow the scenarios below in order.

7. Demo Scenario 1 — Basic Definition Question
User action
Click the button:

What is a Roth IRA?

Expected result

The application generates a retirement-related answer
The answer includes a citation section
The sources are clickable links
The answer shows as Validated when grounded in available sources

What to point out

The system can answer common retirement questions
Answers include source grounding
Users can click citation links to verify the information directly


8. Demo Scenario 2 — Another Button-Based Question
User action
Click the button:

What is a 401(k)?

Expected result

The system returns a clear explanation
The answer includes citations when source support exists
The UI displays supported source links under the answer

What to point out

The application supports multiple retirement concepts
It uses retrieval-based answering, not raw AI generation alone


9. Demo Scenario 3 — Free-Text Question
User action
Type the following into the text box and click Send:

What is the difference between a Roth IRA and a Traditional IRA?

Expected result

The application generates a comparison answer
If enough grounded source content exists, citations appear
If not, the app falls back to general financial knowledge with a note

What to point out

Users are not limited to the preset buttons
The system supports fully custom questions
The fallback system ensures a helpful answer is always returned


10. Demo Scenario 4 — Personalized Scenario Engine
User action
Open the Personalized Scenario: Compound Interest section and enter:
FieldValueAge20Retirement Age65Annual Income70,000Current Savings2,000Monthly Contribution300
Then click Run Scenario.
Expected result

The app calculates a projected retirement balance
The result includes a short plain-English explanation
The response appears in the same styled answer area as other answers

What to point out

This is not just a Q&A bot — it includes a personalized projection workflow
The backend combines compound interest calculation logic with source-based educational context


11. Demo Scenario 5 — Source Verification
User action
Under any generated answer, click one of the source links.
Expected result

The source opens in a new browser tab
The user can inspect the referenced material directly

What to point out

The project supports full transparency
Users can verify exactly where the information came from
This reduces black-box AI behavior and builds trust


12. Demo Scenario 6 — Fallback Behavior
User action
Type the following into the text box and click Send:

How should I think about retirement planning when I am just starting my career?

Expected result

The system still returns a helpful answer
The response may indicate it is based on general financial knowledge rather than directly grounded project sources
The application does not fail or return an empty response

What to point out

The fallback system prevents dead ends
The app remains useful even when exact source retrieval is weak