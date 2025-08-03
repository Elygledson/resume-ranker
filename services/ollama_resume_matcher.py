import json
import requests

import logging
from typing import List
from config import settings
from schemas import SummaryResume
from services.base_resume_matcher import BaseResumeMatcher

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class OllamaResumeMatcher(BaseResumeMatcher):
    def extract_summary_from_resume(self, content: str) -> SummaryResume:
        prompt = f"""
        Você é uma especialista em elaborar resumos de currículos, com grande habilidade para captar o máximo de informações relevantes de cada documento.

        A seguir, está o conteúdo de um currículo profissional:

        {content}

        Extraia as informações conforme o esquema abaixo, com riqueza de detalhes:

        - candidate_name: nome completo do candidato
        - summary: um resumo completo e detalhado, incluindo formação acadêmica, principais experiências profissionais, competências e habilidades.

        Por favor, retorne apenas um JSON que siga esse esquema.
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
        return SummaryResume(**json.loads(response.json()['message']['content']))

    def find_best_match(self, query: str, resumes: List[SummaryResume]) -> str:
        prompt = f"""
            Você é uma especialista em análise de currículos com foco em identificar o candidato mais adequado com base em uma necessidade específica.

            A seguir está a descrição da vaga ou necessidade:
            ---
            {query}
            ---

            Com base nessa necessidade, analise detalhadamente os seguintes currículos, extraídos previamente e já resumidos:

            Resumos:
            {chr(10).join([f"{i+1}. Nome: {r.candidate_name}\nResumo: {r.summary}" for i, r in enumerate(resumes)])}

            Tarefa:
            1. Avalie cada candidato em relação aos requisitos e contexto da vaga.
            2. Identifique o candidato que mais se adequa à descrição fornecida.
            3. Justifique sua escolha com base nas experiências, habilidades ou formação descritas no resumo.
            4. Seja claro, objetivo e completo na justificativa.

            Formato da resposta:
            - Candidato mais adequado: <Nome>
            - Justificativa: <Texto detalhado explicando por que este candidato é o mais adequado em comparação aos demais.>
        """

        logger.info(f'{prompt}')

        response = requests.post(f"{settings.AI_SERVICE_KEY}/generate", json={
            "prompt": prompt,
            "stream": False,
            "model": "llama3.2:latest",
            "options": {
                "temperature": 0.2,
                "repeat_penalty": 1,
            }
        })
        return response.json()['response']
