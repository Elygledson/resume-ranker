import json
import requests

from config import settings
from schemas import SummaryResume


class OllamaService:
    def __init__(self) -> None:
        super().__init__()

    def extract_summary_from_resume(self, content: str) -> SummaryResume:
        prompt = f"""
        A seguir está o conteúdo de um currículo. 
        
        {content}

        Extraia as informações conforme o schema abaixo: 
        Schema:
        candidate_name: Nome do candidato
        summary: Um resumo sobre o candidato, incluindo formação, principais experiências, competências, habilidades.
        """

        response = requests.post(f"{settings.AI_SERVICE_KEY}/chat", json={
            "model": "llama3.2:latest",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "format":  {
                "type": "object",
                "properties": {
                    "candidate_name": {
                        "type": "string",
                    },
                    "summary": {
                        "type": "string",
                    }
                },
                "required": [
                    "candidate_name",
                    "summary"
                ]
            }
        })
        return json.loads(response.json()['message']['content'])

    def find_best_match(self, query: str, resumes: list[SummaryResume]) -> str:
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
