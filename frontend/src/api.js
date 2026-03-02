const API_BASE = "http://127.0.0.1:8000";

const ENDPOINT = "/api/ai/generate"; // change to "/ask" if your backend uses /ask

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