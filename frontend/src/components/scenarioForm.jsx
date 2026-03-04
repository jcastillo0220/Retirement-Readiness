import { useState } from "react";
import {
  scenarioCardStyle,
  scenarioLabelStyle,
  scenarioInputStyle,
  scenarioButtonStyle,
  inputBoxStyle,
} from "../styles";

export default function ScenarioForm({ onSubmit }) {
  const [age, setAge] = useState("");
  const [retirementAge, setRetirementAge] = useState("");
  const [income, setIncome] = useState("");
  const [savings, setSavings] = useState("");
  const [contrib, setContrib] = useState("");
  const [error, setError] = useState("");

  function formatCurrency(value) {
    if (!value) return "";

    // If user is typing a trailing decimal: "42000."
    if (value.endsWith(".")) {
      const [int] = value.split(".");
      const formattedInt = Number(int).toLocaleString("en-US");
      return "$" + formattedInt + ".";
    }

    // If user is typing a partial decimal: "42000.0" or "42000.05"
    if (/^\d+\.\d*$/.test(value)) {
      const [int, dec] = value.split(".");
      const formattedInt = Number(int).toLocaleString("en-US");
      return "$" + formattedInt + "." + dec;
    }

    // Fully valid number → format normally
    const num = Number(value);
    if (isNaN(num)) return value;

    return num.toLocaleString("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    });
  }

  function handleSubmit() {
    if (
      !age ||
      !retirementAge ||
      !income ||
      !savings ||
      !contrib ||
      Number(age) === 0 ||
      Number(retirementAge) === 0 ||
      Number(income) === 0 ||
      Number(savings) === 0 ||
      Number(contrib) === 0
    ) {
      setError("All fields must be greater than zero.");
      return;
    }

    if (Number(retirementAge) <= Number(age)) {
      setError("Retirement age must be greater than current age.");
      return;
    }

    setError("");
    const clean = (v) => {
      const n = Number(v);
      return isNaN(n) ? 0 : n;
    };

    onSubmit({
      age: clean(age),
      retirement_age: clean(retirementAge),
      annual_income: clean(income),
      current_savings: clean(savings),
      monthly_contribution: clean(contrib),
    });

  }

  return (
    <div style={scenarioCardStyle}>
      <h3 style={{ ...scenarioLabelStyle, fontSize: 16, marginBottom: 14 }}>
        Personalized Scenario
      </h3>

      <div style={{ marginBottom: 10 }}>
        <div style={scenarioLabelStyle}>Age</div>
        <input
          type="number"
          min="0"
          max="120"
          step="1"
          style={scenarioInputStyle}
          value={age}
          placeholder="e.g., 42"
          onChange={(e) => {
            const v = e.target.value;
            if (/^\d*$/.test(v)) setAge(v);
          }}
        />
      </div>

        <div style={scenarioLabelStyle}>Target Retirement Age</div>
        <input
          type="number"
          min={Number(age) + 1}
          max="120"
          step="1"
          style={scenarioInputStyle}
          value={retirementAge}
          placeholder="e.g., 67"
          onChange={(e) => {
            const v = e.target.value;
            if (/^\d*$/.test(v)) setRetirementAge(v);
          }}
        />

        <div style={scenarioLabelStyle}>Annual Income</div>
        <input
          style={scenarioInputStyle}
          placeholder="e.g., 55000"
          value={formatCurrency(income)}
          onChange={(e) => {
            const raw = e.target.value.replace(/[^0-9.]/g, "");
            if (/^\d*\.?\d*$/.test(raw)) setIncome(raw);
          }}
        />

        <div style={scenarioLabelStyle}>Current Savings</div>
        <input
          style={scenarioInputStyle}
          placeholder="e.g., 15000"
          value={formatCurrency(savings)}
          onChange={(e) => {
            const raw = e.target.value.replace(/[^0-9.]/g, "");
            if (/^\d*\.?\d*$/.test(raw)) setSavings(raw);
          }}
        />

        <div style={scenarioLabelStyle}>Monthly Contribution</div>
        <input
          style={scenarioInputStyle}
          placeholder="e.g., 300"
          value={formatCurrency(contrib)}
          onChange={(e) => {
            const raw = e.target.value.replace(/[^0-9.]/g, "");
            if (/^\d*\.?\d*$/.test(raw)) setContrib(raw);
          }}
        />

        {error && (
          <div style={{ color: "#b00020", marginBottom: 10, fontSize: 13 }}>
            {error}
          </div>
        )}

        <button style={scenarioButtonStyle} onClick={handleSubmit}>
          Run Scenario
        </button>
      </div>
   );
}