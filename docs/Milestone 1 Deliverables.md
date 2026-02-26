# Milestone 1 Deliverables  
## Team: Retirement Readiness  
### Focus: Grounded, Personalized Retirement Planning Assistant  

---

## Context

During the Spike demo, the team demonstrated:

- A user can ask retirement-related questions (e.g., “What is a Roth IRA?”)  
- The LLM generates explanations  
- The response references external financial sources (e.g., Fidelity website)

However:

- The system primarily explains financial terms (generic knowledge)  
- There is no structured citation mechanism  
- There is no verification layer  
- There is no personalization using user-specific financial data  
- There is no measurable evaluation of grounding accuracy  

Milestone 1 must elevate this from a generic term-explainer to a **grounded, verifiable, and partially personalized retirement assistant.**

---

# Milestone 1 Objective

By Milestone 1, your team must demonstrate:

- A working Retrieval-Augmented Generation (RAG) pipeline  
- Structured ingestion of trusted retirement sources  
- Explicit citation formatting in answers  
- A validation layer preventing unsupported claims  
- A personalized “retirement scenario explanation” component  
- Measurable evaluation metrics  
- Clean GitHub structure + technical walkthrough video  

---

# 1. Updated PRD-Lite (1–2 pages)

Your PRD must clearly define the product as:

> A grounded retirement planning assistant that explains concepts and provides scenario-based insights using verified financial sources.

## The PRD must include:

### A. Expanded Value Beyond Definitions

You must go beyond explaining terms. Include at least one of:

- Scenario-based projections (e.g., “If you invest $X per month…”)  
- Rule-based retirement readiness checks  
- Age-based planning recommendations  
- Contribution limit analysis  
- Roth vs Traditional comparison using structured logic  

### B. Grounding Requirement (Non-Negotiable)

- Every answer must include citation markers  
- Answers must be traceable to retrieved source documents  
- No unsupported financial claims  
- If no verified source is found, the system must refuse  

### C. Acceptance Criteria (Testable)

Examples:

- 100% of answers contain citations  
- 0 unsupported financial statements  
- Refusal triggered when no relevant source exists  
- ≥ 85% retrieval accuracy on test set  

---

# 2. Structured Data & Source Indexing

You must create:

/docs/data_sources.md  

This must list:

- Source URLs (Fidelity, IRS, government retirement resources, etc.)  
- Date accessed  
- Type of document  
- Preprocessing notes  

You must document:

- Chunking strategy  
- Embedding strategy  
- Retrieval configuration (top-k, similarity metric)

---

# 3. Citation & Verification Layer (Required)

Implement:

/src/citation_formatter.py  
/src/validator.py  

The system must:

- Display citation markers (e.g., [1], [2])  
- Map citations to retrieved documents  
- Prevent statements not present in retrieved context  

Validation must include:

- Checking that all numeric claims appear in retrieved sources  
- Ensuring all references correspond to indexed documents  

Manual review is not acceptable.

---

# 4. Personalized Scenario Engine (Required Upgrade)

To add meaningful value beyond term explanation, implement:

/src/scenario_engine.py  

This component must:

- Accept user inputs such as:
  - Age
  - Annual income
  - Current savings
  - Monthly contribution
- Apply deterministic financial formulas (e.g., compound growth)
- Pass structured outputs to LLM for explanation

The LLM must explain results, not compute them.

Example:

Deterministic calculation → projected retirement fund  
LLM → explains implications + cites financial rules  

---

# 5. Evaluation Starter Kit (Minimum 20 Test Questions)

Create:

/docs/evaluation_test_cases.md  

Include:

- 20 retirement-related queries  
- Expected source documents  
- Retrieved documents  
- Generated answer  
- Citation verification result  
- Pass/Fail grounding  

Required metrics:

- Retrieval accuracy  
- Citation accuracy  
- Grounding pass rate  
- Refusal accuracy  

---

# 6. Spike Update Document

Create:

/docs/spike_results.md  

Must include:

- What worked in explanation demo  
- Identified simplicity limitation  
- Need for citation + validation  
- Architecture upgrade plan  
- Scenario engine addition  

---

# 7. Architecture Diagram (1 page)

Create:

/docs/architecture.png  

Must clearly show:

User Question  
→ Query Embedding  
→ Vector Search  
→ Retrieved Documents  
→ Deterministic Financial Logic (if scenario-based)  
→ LLM Explanation  
→ Citation Formatter  
→ Validation Layer  
→ Output  

Label deterministic vs generative components.

---

# 8. Required Technical Walkthrough Video (No UI Required)

Submit a 5–8 minute technical walkthrough video showing:

- Document ingestion  
- Retrieval results in logs  
- Citation formatting  
- Validation layer logic  
- Scenario engine calculations  
- Refusal example  

UI polish is NOT required. Engineering demonstration is required.

Store in:

/docs/demo_video.mp4  

or link externally.

---

# 9. GitHub Repository Requirements

Your repository must include:

- /docs/PRD.md  
- /docs/data_sources.md  
- /docs/spike_results.md  
- /docs/evaluation_test_cases.md  
- /docs/architecture.png  
- /src/retrieval.py  
- /src/generator.py  
- /src/citation_formatter.py  
- /src/validator.py  
- /src/scenario_engine.py  

Additionally:

- Updated README with setup and run instructions  
- requirements.txt  
- .env.example  
- At least one meaningful commit per team member  
- Sprint 1 issue board with assigned owners  

---

# Required Live Demo for Milestone 1

You must demonstrate:

1. A retirement-related question  
2. Retrieved documents displayed  
3. Generated answer with citations  
4. Validation layer running  
5. A personalized scenario explanation  
6. A refusal case when unsupported  

If answers are generic explanations without structured citation and validation, Milestone 1 is incomplete.

---

# Milestone 1 Standard

Your project must evolve from:

“We explain retirement terms using an LLM.”  

To:

“We engineered a grounded, citation-based retirement assistant with validation and scenario-based financial logic.”  

This is the expected senior-level outcome.
