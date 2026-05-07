import requests
import os

GEMINI_API_KEY = "AIzaSyBaXoQYjgtaAhIN6jSfvPTOhvnPYSgcam4"

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"


def generate_answer(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("ERROR:", response.text)
        return "LLM request failed"

    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "Failed to parse response"