# Spike Results

## What Worked in Explanation Demo
- The frontend was able to communicate effectively to the backend and the LLM: Gemini 2.5 Flash
- Gemini explained each retirement plan correct and in a short amount of time
- Suggested follow-up buttons were generated based on what retirement plan the user clicked

## Identified Simplicity Limitation
- Gemini generated a very simple explaniation of the different retirement plans
- LLM relied only on the websites' links to generate an explanation
- System lacked any validation to check if the definition was absolutely correct

## Need for Citation + Validation
- Explanations must refrence the source that it is based on
    - Citation formatter must be included to ensure proper citations
- Validation layer included to repair prompts if response gives any invalid definitions

## Architecture Upgrade Plan
- Current architecture:
    - User question -> query prompt -> LLM explanation -> Output
- Creating a new architecture that involves a:
    - Query Classifcation between definitions and a scenario application
    - Proper document retrival through a chunking strategy 
    - Keyword-based retrieval on query prompt
    - Validation layer to repair prompts
    - Finanical Scenario with deterministic logic 

## Scenario engine addition
- Implement a scenario engine that:
    - Relies on a deterministic forumla
    - Allows custom user inputs
    - Room for future expansion of the scenario
    - Return user results + projections and a generative summary
- Scenario engine must include proper citations for explanations
- Scenario engine will never perform any calculations 