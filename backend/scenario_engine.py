def compute_projection(
    age: int,
    annual_income: float,
    current_savings: float,
    monthly_contribution: float,
    retirement_age: int = 67,
    return_rate: float = 0.05
):
    if age < 0 or retirement_age <= age:
        raise ValueError("Invalid age or retirement age.")

    years = retirement_age - age
    r = return_rate
    P = current_savings
    C = monthly_contribution

    # Compound growth on current savings
    future_principal = P * ((1 + r) ** years)

    # Future value of monthly contributions
    future_contrib = C * 12 * (((1 + r) ** years - 1) / r)

    projected = future_principal + future_contrib

    return {
        "age": age,
        "retirement_age": retirement_age,
        "years_to_grow": years,
        "annual_income": annual_income,
        "current_savings": current_savings,
        "monthly_contribution": monthly_contribution,
        "assumed_return_rate": return_rate,
        "projected_balance": round(projected, 2),
    }