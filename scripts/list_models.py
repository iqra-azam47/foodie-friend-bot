"""Prints the Gemini models your API key can use.
Run from the project folder with:  python scripts/list_models.py"""
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Models that can chat with your key:")
for model in client.models.list():
    if "generateContent" in (model.supported_actions or []):
        print(" -", model.name.replace("models/", ""))
