def generate_suggestions(answer: str):
    answer_lower = answer.lower()
    suggestions = []

    for keyword, prompts in generator_map.items():
        if keyword in answer_lower:
            suggestions.extend(prompts)

    return suggestions

generator_map = {
    "tax": [
        {
            "label": "How do taxes work in a Roth IRA?",
            "prompt": "How do taxes work in a Roth IRA?"
        },
        {
            "label": "What are the tax advantages?",
            "prompt": "What are the tax advantages of a Roth IRA?"
        }
    ],
    "withdraw": [
        {
            "label": "What are qualified withdrawals?",
            "prompt": "What are qualified withdrawals in a Roth IRA?"
        },
        {
            "label": "What happens if I withdraw early?",
            "prompt": "What happens if I withdraw from a Roth IRA early?"
        }
    ],
    "contribution": [
        {
            "label": "What are contribution limits?",
            "prompt": "What are the Roth IRA contribution limits?"
        }
    ],
    "ira": [
        {
            "label": "What is an IRA?",
            "prompt": "What is an IRA?"
        },
        {
            "label": "Explain Roth vs Traditional IRA.",
            "prompt": "What is the difference between a Roth IRA and a Traditional IRA?"
        }
    ],
}