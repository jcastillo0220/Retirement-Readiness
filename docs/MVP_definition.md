# MVP Definition — Retirement Readiness (Milestone 2) (Submitted Late (4/6))

## 1. MVP Workflows Included
The MVP supports **two core workflows**, each grounded, validated, and citation‑driven.

### 1.1 Definition Workflow (RAG Explanation)
Users select a retirement topic (e.g., Roth IRA, 401(k), Traditional IRA) and receive:

- A grounded explanation sourced from trusted PDFs  
- Inline citation markers  
- A grounding report validating each phrase  
- Automatic refusal when AI fails to replicate a valid answer after 3 attempts

### 1.2 Scenario Workflow (Deterministic Projection + Explanation)
Users enter personal financial inputs:

- Age  
- Retirement age  
- Annual income  
- Current savings  
- Monthly contribution  

The backend:

1. Computes a deterministic projection using numeric rules  
2. Retrieves relevant numeric rule chunks  
3. Generates an LLM explanation grounded strictly to those rules  
4. Returns a citation‑validated explanation  

---

## 2. What Users Can Do in the MVP
The MVP enables users to:

- Select a retirement topic and receive a **cited, grounded definition**  
- Enter personal financial inputs and receive a **deterministic projection**  
- View a **grounding report** showing supported vs unsupported phrases  
- See **citation markers** linking to authoritative sources  
- Receive **refusals** when no supporting source exists  
- Interact with a UI that highlights grounded text and chunk evidence  

---

## 3. Explicitly Out of Scope for Milestone 2
The following features are **not included**:

- Real‑time financial data retrieval  
- Personalized long‑term financial planning or advice  
- User accounts, authentication, or saved scenarios  
- Uploading custom documents  
- Multi‑source blending beyond approved PDFs and numeric rules  
- Tax optimization or personalized recommendations  

---

## 4. Supported Source Types and Their Roles

| Source Type | Role in MVP | Examples |
|-------------|-------------|----------|
| **PDFs (trusted retirement sources)** | Provide authoritative definitions and explanations | Northwestern Mutual |
| **Numeric rule documents** | Provide deterministic formulas for projections and authoritative definitions and explanations | Fidelity, IRS |
| **No external web search** | Prevents hallucination and ensures grounding | N/A |

**PDFs = definitions**  
**Numeric rules = definitions + projections**

---

## 5. Known Limitations
The MVP has the following constraints:

- Explanations cannot reference concepts not present in retrieved chunks  
- Scenario projections are deterministic (no inflation, no risk modeling)  
- Retrieval quality depends on chunking; missing chunks reduce grounding accuracy  
- Unsupported queries result in refusals, even if the answer is “common knowledge” (excluding website for definiton)
- Key phrase extraction may occasionally over‑ or under‑segment phrases  
- PDF definitions may be outdated within 3-5 years, its numeric outputs outdated in a year

---

## 6. Definition of Done (DoD)

### Functional Requirements
- Both workflows (definition + scenario) run end‑to‑end  
- All answers include citation markers  
- Grounding report generated for every answer  
- Unsupported queries trigger a refusal  
- Deterministic projection logic validated and correct  

### Technical Requirements
- Retrieval accuracy meets baseline threshold  
- Grounding accuracy measured and logged  
- Hallucination rate below defined tolerance  
- Refusal accuracy validated with test queries  
- Prompts enforce grounding and citation rules  
- UI displays:  
  - Answer bubble  
  - Citations  
  - Grounding report  
  - Supported/unsupported phrases   

### Quality Requirements
- No hallucinated claims in validated answers  
- All explanations reference only approved sources  
- UI is stable, readable, and consistent  