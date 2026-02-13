from google import genai

client = genai.Client(api_key="AIzaSyBi0DfWxHxI7vKpnJpr1jq1NdArw-vEK6w")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Say hello in a creative way."
)

print(response.text)