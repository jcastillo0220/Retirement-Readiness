from fastapi import FastAPI, Request
from google import genai

# uvicorn endpoint:app --reload
# ^This will run the program in development mode. Open http://localhost:8000/docs to view the API documentation and test the endpoint.

# Do not share this API key with anyone. Keep it secret and secure.
API_KEY = "AIzaSyDLXw7TU7ntqZ52NhZ-bNO72qThVNs9I6I"
client = genai.Client(api_key=API_KEY)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/ai/generate")
async def generate(req: Request):
    data = await req.json()
    user_question = data["question"]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_question
    )

    return {"answer": response.text}