## **Validation Architecture**  
The system uses two validation layers. validator.py checks citation format and performs numeric cross‑checks to ensure all cited sources and numbers appear in the retrieved chunks. grounding_verifier.py handles phrase‑level grounding by extracting key content phrases and confirming each one is supported by at least one retrieved chunk. The /api/scenario endpoint now relies mainly on the grounding verifier for semantic accuracy, while the validator enforces citation and numeric correctness. Both validation results are returned to the frontend so it can decide whether to show the answer or trigger a repair cycle.

### **Validator Responsibilities (validator.py)**  
- Ensures citations reference only retrieved sources
- Ensures Markdown links (or allowed alternatives) are present
- Normalizes citation phrases for matching
- Extracts all numbers from the answer
- Extracts all numbers from retrieved chunks
- Flags any number not found in the sources
- Ensures citation map and natural‑language citations agree
- This validator focuses on format, structure, and numeric safety.

### **Grounding Verifier Responsibilities (grounding_verifier.py)**  
- Cleans the answer (removes citation line, sources block, markdown links)
- Extracts meaningful 3–4 word content phrases
- Filters out stopwords and trivial phrases
- Computes phrase‑level support using overlap scoring
- Flags unsupported claims even if citations look correct
- Returns a full grounding report:
    - Supported phrases
    - Unsupported phrases
    - Chunk‑level evidence  

This verifier focuses on semantic grounding and content accuracy.

### **How Validation Results Reach the Frontend**

Both validators run before the final answer is returned.
The backend returns a structured response:

<pre>
{
  "answer": "...",
  "projection": {...},
  "ai_explanation": "...",
  "validation": {
    "citation_validator": { ... },
    "grounding_verifier": { ... }
  }
}
</pre>

The frontend uses this to decide whether to:  
- Display the answer 
- Show a fallback
- Or request a repaired answer

### **Call Path for a Single Request**

<pre>
User Input  
    ↓  
Frontend → /api/scenario  
    ↓  
Backend computes deterministic projection (no AI math)  
    ↓  
Backend retrieves trusted source chunks  
    ↓  
LLM generates explanation (no numbers, no tables)  
    ↓  
validator.py  
  - Citation format check  
  - Numeric cross-check  
    ↓  
grounding_verifier.py  
  - Phrase-level grounding check  
    ↓  
If both pass → return final answer to frontend  
If either fails → repair prompt → LLM → revalidate → return
</pre>

