const API_BASE = import.meta.env.VITE_API_URL;

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