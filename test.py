from google import genai

# Do not share this API key with anyone. Keep it secret and secure.
API_KEY = "AIzaSyDLXw7TU7ntqZ52NhZ-bNO72qThVNs9I6I"
client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="can you explain what Roth IRA as simple and formally as you can. " \
    "Make it as short as possible and use simple language. \
        Do not include an example."
)

print("/n", response.text)