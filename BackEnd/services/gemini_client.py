import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
APIKEY = os.getenv("GEMINI_API_KEY")


if not APIKEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables")


genai.configure(api_key=APIKEY)


class GeminiClient:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(self.model_name)

    def __str__(self):
        return self.model_name
    
    def generate_content(self, prompt:str)->str:
        return self.model.generate_content(prompt)