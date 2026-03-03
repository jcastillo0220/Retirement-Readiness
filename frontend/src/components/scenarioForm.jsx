import { useState } from "react";

export default function ScenarioForm({ onSubmit }) {
  const [age, setAge] = useState("");
  const [income, setIncome] = useState("");
  const [savings, setSavings] = useState("");
  const [contrib, setContrib] = useState("");

  return (
    <div style={{ marginBottom: 20, padding: 10 }}>
      <h3>Personalized Scenario</h3>

      <input placeholder="Age" value={age} onChange={(e) => setAge(e.target.value)} />
      <input placeholder="Annual income" value={income} onChange={(e) => setIncome(e.target.value)} />
      <input placeholder="Current savings" value={savings} onChange={(e) => setSavings(e.target.value)} />
      <input placeholder="Monthly contribution" value={contrib} onChange={(e) => setContrib(e.target.value)} />

      <button onClick={() => onSubmit({ age, income, savings, contrib })}>
        Run Scenario
      </button>
    </div>
  );
}