import requests

from config import settings


class OllamaService:
    def __init__(self) -> None:
        super().__init__()

    def generate_structured_output(self, prompt: str, schema: dict) -> str:
        response = requests.post(f"{settings.AI_SERVICE_KEY}/generate", json={
            "model": "llama3.2:latest",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "format": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "capital": {
                        "type": "string"
                    },
                    "languages": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "name",
                    "capital",
                    "languages"
                ]
            }
        })
        return response.json()['response']

    def generate(self, query: str) -> str:
        response = requests.post(f"{settings.AI_SERVICE_KEY}/generate", json={
            "prompt": query,
            "stream": False,
            "model": "llama3.2:latest",
            "options": {
                "temperature": 0.2,
                "repeat_penalty": 1,
            }
        })
        return response.json()['response']
