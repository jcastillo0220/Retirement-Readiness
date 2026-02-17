from fastapi import FastAPI, Request
from google import genai

# Do not share this API key with anyone. Keep it secret and secure.
API_KEY = "AIzaSyDLXw7TU7ntqZ52NhZ-bNO72qThVNs9I6I"
client = genai.Client(api_key=API_KEY)

app = FastAPI()
model = genai.GenerativeModel("gemini-2.0-flash")

@app.post("/api/ai/generate")
async def generate(req: Request):
    data = await req.json()
    user_question = data["question"]

    prompt = f"""
    You are a financial education assistant.
    Question: {user_question}
    Provide beginner-friendly guidance.
    """

    response = model.generate_content(prompt)

    return {"answer": response.text}