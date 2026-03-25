const API_BASE = "http://localhost:8000";

const ENDPOINT = "/api/ai/generate"; 

export async function askAI(payload) {
  const res = await fetch(`${API_BASE}${ENDPOINT}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const text = await res.text();

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${text}`);
  }

  return JSON.parse(text);
}

export async function runScenario(inputs) {
  const res = await fetch("http://localhost:8000/api/scenario", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputs),
  });

  if (!res.ok) throw new Error("Scenario error");
  return res.json();
}