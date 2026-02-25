from typing import Optional

generator_map = {
    "roth_ira": [
        {"label": "How do taxes work in a Roth IRA?", "prompt": "How do taxes work in a Roth IRA?"},
        {"label": "What are qualified withdrawals?", "prompt": "What are qualified withdrawals in a Roth IRA?"},
        {"label": "What are contribution limits?", "prompt": "What are the Roth IRA contribution limits?"},
        {"label": "Roth vs Traditional IRA", "prompt": "What is the difference between a Roth IRA and a Traditional IRA?"}
    ],
    "401k": [
        {"label": "How does a 401(k) work?", "prompt": "How does a 401(k) work?"},
        {"label": "What are 401(k) tax rules?", "prompt": "How are 401(k) contributions and withdrawals taxed?"}
    ],
    "traditional_ira": [
        {"label": "How are Traditional IRAs taxed?", "prompt": "How are Traditional IRAs taxed?"},
        {"label": "Traditional IRA contribution rules", "prompt": "What are the contribution rules for a Traditional IRA?"}
    ],
    "rollover_ira": [
        {"label": "What is a Rollover IRA?", "prompt": "What is a Rollover IRA?"},
        {"label": "When to use a Rollover IRA", "prompt": "When should someone use a Rollover IRA?"}
    ],
    "roth_401k": [
        {"label": "What is a Roth 401(k)?", "prompt": "What is a Roth 401(k)?"},
        {"label": "Roth 401(k) vs Roth IRA", "prompt": "How is a Roth 401(k) different from a Roth IRA?"}
    ],
}

keyword_map = {
    "401k": "401k",
    "401(k)": "401k",
    "roth 401": "roth_401k",
    "roth 401k": "roth_401k",
    "roth ira": "roth_ira",
    "traditional": "traditional_ira",
    "rollover": "rollover_ira",
    "rollover ira": "rollover_ira",
    "traditional ira": "traditional_ira",
    "ira": "roth_ira",
}

def generate_suggestions(answer: str, topic_key: Optional[str] = None):
    if topic_key:
        normalized = topic_key.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
        if normalized in generator_map:
            return generator_map[normalized]
        alias_map = {
            "what is a roth ira?": "roth_ira",
            "what is a 401(k)?": "401k",
            "what is a traditional ira?": "traditional_ira",
            "what is a rollover ira?": "rollover_ira",
            "what is a roth 401(k)?": "roth_401k",
        }
        if topic_key.lower() in alias_map:
            return generator_map.get(alias_map[topic_key.lower()], [])

    answer_lower = (answer or "").lower()
    for kw, topic in keyword_map.items():
        if kw in answer_lower:
            return generator_map.get(topic, [])

    return [
        {"label": "What is an IRA?", "prompt": "What is an IRA?"},
        {"label": "What are contribution limits?", "prompt": "What are retirement account contribution limits?"}
    ]