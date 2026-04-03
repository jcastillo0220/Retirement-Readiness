export const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const ENDPOINT = "/api/ai/generate";

console.log("API_BASE =", API_BASE);

async function parseJsonResponse(res, fallbackLabel = "Request failed") {
  const text = await res.text();

  if (!res.ok) {
    throw new Error(`${fallbackLabel}: HTTP ${res.status}: ${text}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`Invalid JSON response: ${text}`);
  }
}

export async function askAI(payload) {
  const res = await fetch(`${API_BASE}${ENDPOINT}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  return parseJsonResponse(res, "AI request failed");
}

export async function runScenario(inputs) {
  const res = await fetch(`${API_BASE}/api/scenario`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputs),
  });

  return parseJsonResponse(res, "Scenario error");
}