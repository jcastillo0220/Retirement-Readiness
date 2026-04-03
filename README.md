# Retirement Readiness
Our venture helps prepare individuals who are on a path to retirement and want to be educated in various retirement plans. 

---

## Team Members & Roles
- **Javier Castillo** — Project Lead
- **Joaquin Castillo** — AI Dev
- **Abcde Mireles** — UI Designer
- **Jose Torres** — Data Gatherer

---
## Link to Latest Docs
[**PRD**](https://github.com/jcastillo0220/Retirement-Readiness/blob/main/docs/PRD.pdf)<br>
[**Spike Plan**](https://github.com/jcastillo0220/Retirement-Readiness/blob/main/docs/Spike%20Plan.pdf)<br>
[**Pitch Deck**](https://github.com/jcastillo0220/Retirement-Readiness/blob/bbb02bedf890d70adcc42897e60de980f2cbb1ea/docs/Pitch%20Deck.pdf)<br>

## Overview
The Retirement Readiness application is a full-stack web application designed to help users understand key retirement concepts and explore personalized financial scenarios.

The system combines:
- A FastAPI backend with AI-powered responses
- A React + Vite frontend for user interaction
- A retrieval-based system using curated financial sources
- A fallback AI system to ensure users always receive an answer

---

## Features

### AI-Powered Q&A
- Answers retirement-related questions (e.g., Roth IRA, 401(k))
- Uses grounded sources when available
- Falls back to general financial knowledge when sources are insufficient

### Source Grounding and Validation
- Answers are validated against provided source documents
- Displays supported phrases and confidence levels
- Prevents unsupported or hallucinated responses

### Personalized Scenario Engine
- Calculates retirement projections based on:
  - Age
  - Retirement age
  - Income
  - Savings
  - Monthly contributions

### Caching System
- Stores responses to improve performance
- Reduces repeated API calls

---

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Google Generative AI (Gemini)
- BeautifulSoup
- PyPDF2

### Frontend
- React
- Vite
- Tailwind CSS

---

## Project Structure

```
Retirement-Readiness/
│
├── backend/
│   ├── endpoint.py
│   ├── chunking.py
│   ├── cache.py
│   ├── validator.py
│   ├── grounding_verifier.py
│   ├── requirements.txt
│   └── .env (not committed)
│
├── frontend/
│   ├── src/
│   ├── package.json
│
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

---

## Backend Setup

1. Navigate to backend:
```bash
cd backend
```

2. Create virtual environment:
```bash
python3 -m venv .venv
```

3. Activate environment:

Mac/Linux:
```bash
source .venv/bin/activate
```

Windows:
```bash
.venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a file:
```
backend/.env
```

Add your API key:
```
GOOGLE_API_KEY=your_api_key_here
```

Important:
- Do not commit `.env`
- It is already ignored in `.gitignore`

---

## Run Backend

```bash
python3 -m uvicorn endpoint:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

## Frontend Setup

Open a new terminal.

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run frontend:
```bash
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

---

## How It Works

1. User submits a question
2. Backend retrieves relevant source chunks
3. AI generates an answer using those sources
4. Validation checks grounding and accuracy
5. If no sources are found, fallback AI generates a general answer
6. Response is cached and returned to frontend

---

## Fallback System

If no relevant source data is found:
- The system generates an answer using general financial knowledge
- The response is clearly labeled as not source-grounded

This ensures:
- The user always receives an answer
- The system remains usable even with limited data

---

## Security Practices

- API keys stored in `.env`
- `.env` excluded via `.gitignore`
- No sensitive data committed to repository

---

## Common Issues

### Missing dependencies
Run:
```bash
pip install -r requirements.txt
```

### Module not found errors
Ensure virtual environment is activated.

### API errors
Verify `.env` file exists and contains a valid API key.

---

## Future Improvements

- Add more financial data sources
- Improve retrieval accuracy
- Enhance UI feedback for fallback responses
- Add authentication and user profiles

---

## License
This project is for educational purposes.