import { useState } from "react";
import {
  scenarioCardStyle,
  scenarioLabelStyle,
  scenarioInputStyle,
  scenarioButtonStyle,
  dropdownHeaderStyle,
  dropdownBodyStyle,
} from "../styles";

export default function ScenarioForm({ onSubmit, loading }) {
  const [open, setOpen] = useState(false);

  const [age, setAge] = useState("");
  const [retirementAge, setRetirementAge] = useState("");
  const [income, setIncome] = useState("");
  const [savings, setSavings] = useState("");
  const [contrib, setContrib] = useState("");
  const [error, setError] = useState("");

  function formatCurrency(value) {
    if (!value) return "";

    if (value.endsWith(".")) {
      const [int] = value.split(".");
      const formattedInt = Number(int).toLocaleString("en-US");
      return "$" + formattedInt + ".";
    }

    if (/^\d+\.\d*$/.test(value)) {
      const [int, dec] = value.split(".");
      const formattedInt = Number(int).toLocaleString("en-US");
      return "$" + formattedInt + "." + dec;
    }

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

    const clean = (v) => {
      const n = Number(v);
      return isNaN(n) ? 0 : n;
    };

    setError("");
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
      {/* Dropdown Header */}
      <div style={dropdownHeaderStyle} onClick={() => setOpen(!open)}>
        <span>Personalized Scenario: Compound Interest</span>
        <span
          style={{
            transform: open ? "rotate(90deg)" : "rotate(0deg)",
            transition: "0.2s",
          }}
        >
          ▶
        </span>
      </div>

      {/* Dropdown Body */}
      <div style={dropdownBodyStyle(open)}>
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

        <button
          style={{
            ...scenarioButtonStyle,
            opacity: loading ? 0.6 : 1,
            cursor: loading ? "not-allowed" : "pointer",
          }}
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Running…" : "Run Scenario"}
        </button>
      </div>
    </div>
  );
}