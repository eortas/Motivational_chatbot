import requests
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_motivational_response(estado_emocional):
    prompt = (
        f"El usuario escribió: '{estado_emocional}'. "
        "Devuélveme un mensaje motivacional breve (máximo dos frases), empático y alentador."
    )
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]