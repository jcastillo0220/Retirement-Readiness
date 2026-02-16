from google import genai

API_KEY = "AIzaSyDLXw7TU7ntqZ52NhZ-bNO72qThVNs9I6I"

client = genai.Client(api_key=API_KEY)
print("Using API key:", API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in a creative way."
)

print(response.text)