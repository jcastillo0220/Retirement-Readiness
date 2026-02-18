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
            "prompt": "Explain how taxes work for a Roth IRA as short as possible and use simple language. "
                        "Do not include any examples."
        },
        {
            "label": "What are the tax advantages?",
            "prompt": "Explain the tax advantages of a Roth IRA as short as possible and use simple language. "
                        "Do not include any examples."
        }
    ],
    "withdraw": [
        {
            "label": "What are qualified withdrawals?",
            "prompt": "Explain qualified withdrawals for a Roth IRA as short as possible and use simple language. "
                        "Do not include any examples."
        },
        {
            "label": "What happens if I withdraw early?",
            "prompt": "Explain early withdrawal penalties for a Roth IRA as short as possible and use simple language. "
                        "Do not include any examples."
        }
    ],
    "contribution": [
        {
            "label": "What are contribution limits?",
            "prompt": "Explain Roth IRA contribution limits as short as possible and use simple language. "
                        "Do not include any examples."
        }
    ],
    "ira": [
        {
            "label": "What is an IRA?",
            "prompt": "Explain what an IRA as short as possible and use simple language. "
                        "Do not include any examples."
        },
        {
            "label": "Explain Roth vs Traditional IRA.",
            "prompt": "Compare Roth IRA and Traditional IRA as short as possible and use simple language. "
                        "Do not include any examples."
        }
    ],
}