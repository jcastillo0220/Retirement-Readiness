def compute_projection(
    age: int,
    retirement_age: int,
    current_savings: float,
    monthly_contribution: float,
    return_rate: float = 0.035
):
    if age < 0 or retirement_age <= age:
        raise ValueError("Invalid age or retirement age.")

    years = retirement_age - age
    r = return_rate
    P = current_savings
    PMT = monthly_contribution

    # Compound Interest Formula: A = P(1 + r/n)^(nt)
    # Since we are compounding monthly, n = 12, and t = years
    A = P * ((1 + r / 12) ** (12 * years))
    future_value = A + PMT * (((1 + r / 12) ** (12 * years) - 1) / (r / 12))

    return {
        "age": age,
        "retirement_age": retirement_age,
        "years_to_grow": years,
        "current_savings": current_savings,
        "monthly_contribution": monthly_contribution,
        "assumed_return_rate": return_rate,
        "projected_balance": future_value,
    }