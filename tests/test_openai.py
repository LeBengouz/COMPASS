import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-5-mini",
    input="Réponds uniquement par : connexion réussie"
)

print(response.output_text)