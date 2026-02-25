export async function askAI(payload) {
  const res = await fetch("http://localhost:8000/api/ai/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}