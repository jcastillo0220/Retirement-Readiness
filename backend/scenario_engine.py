def compute_projection(
    age: int,
    retirement_age: int,
    annual_income: float,
    current_savings: float,
    monthly_contribution: float,
    return_rate: float = 0.05
):
    if age < 0 or retirement_age <= age:
        raise ValueError("Invalid age or retirement age.")

    years = retirement_age - age
    r = return_rate
    P = current_savings
    C = monthly_contribution

    # Compound Interest Formula: A = P(1 + r/n)^(nt)
    # Since we are compounding monthly, n = 12, and t = years
    compound_projection = P * ((1 + r / 12) ** (12 * years))

    return {
        "age": age,
        "retirement_age": retirement_age,
        "years_to_grow": years,
        "annual_income": annual_income,
        "current_savings": current_savings,
        "monthly_contribution": monthly_contribution,
        "assumed_return_rate": return_rate,
        "projected_balance": compound_projection,
    }