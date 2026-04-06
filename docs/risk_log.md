# Risk Log – Retirement Readiness Project

## 1. Technical Risks
### R1 — Grounding Mismatch or False “Supported” Flags
**Description:** Phrase matcher may mark phrases as supported even when the chunk only loosely implies the meaning.  
**Impact:** Users may trust grounding that is not fully literal.  
**Likelihood:** Medium  

### R2 — Highlighting Fails for Multi‑Line or Fragmented Text
**Description:** Chunk formatting (line breaks, bullets) may prevent phrase highlighting.  
**Impact:** Users may not see why a phrase is supported.  
**Likelihood:** Medium 

### R3 — Over‑Aggressive Validator Shortens Answers
**Description:** Validator rewrites answers even when the model’s answer is correct.  
**Impact:** Loss of nuance; overly short or generic answers.  
**Likelihood:** High   

### R4 — UI Rendering Issues (HTML, Markdown, Raw Text)
**Description:** ReactMarkdown may escape HTML or fail to render highlights.  
**Impact:** Poor grounding visibility; confusing UX.  
**Likelihood:** Low  

---

## 2. Data and Compliance Risks

### R5 — Incorrect Financial Interpretation
**Description:** Model may paraphrase IRS rules incorrectly if grounding fails.  
**Impact:** User misunderstanding of retirement rules.  
**Likelihood:** Medium  

### R6 — Outdated Source Material
**Description:** IRS limits and definitions may change annually.  
**Impact:** Outdated or incorrect financial guidance. Especially for PDF
**Likelihood:** High  

### R7 — Over‑Reliance on Model Output
**Description:** Users may treat the assistant as financial advice.  
**Impact:** Misinterpretation of guidance.  
**Likelihood:** Medium  

### R8 — Scenario Engine Miscalculations
**Description:** Incorrect compounding logic or parameter parsing.  
**Impact:** Wrong projections lead to user confusion.  
**Likelihood:** Low

---

## 3. UX and Interaction Risks

### R9 — Grounding Report Overload
**Description:** Long chunks may overwhelm users visually.  
**Impact:** Cognitive overload; reduced trust.  
**Likelihood:** Medium  

---

## 4. Operational Risks

### R10 — Backend Latency or Timeouts
**Description:** Chunk retrieval, validation, and rewriting may increase latency.  
**Impact:** Slow responses and overall degraded UX.  
**Likelihood:** High  

### R11 — Dependency Drift
**Description:** ReactMarkdown, rehypeRaw, or backend libraries may change behavior.  
**Impact:** Rendering bugs; broken highlighting.  
**Likelihood:** Medium  

---