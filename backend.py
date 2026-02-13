from google import genai

client = genai.Client(api_key="AIzaSyCaB0DSWgeUfLNaFj9EzFq6vkdhYeJMirk")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Say hello in a creative way."
)

print(response.text)