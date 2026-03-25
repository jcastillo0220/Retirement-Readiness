def compute_projection(
    age: int,
    retirement_age: int,
    annual_income: float,
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

    # Compound interest on current savings
    A = P * ((1 + r / 12) ** (12 * years))

    # Future value of monthly contributions
    future_contribution = PMT * (((1 + r / 12) ** (12 * years) - 1) / (r / 12))

    future_value = round(A + future_contribution, 2)

    projection = {
        "age": age,
        "retirement_age": retirement_age,
        "years_to_grow": years,
        "annual_income": annual_income,
        "current_savings": current_savings,
        "monthly_contribution": monthly_contribution,
        "assumed_return_rate": return_rate,
        "projected_balance": future_value,
    }

    explanation = (
        f"With {years} years until retirement, your savings and monthly "
        f"contributions could grow to about ${future_value:,} assuming a "
        f"{return_rate*100:.1f}% annual return compounded monthly."
    )

    return projection, explanation