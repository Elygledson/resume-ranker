import json
import logging
import requests
import numpy as np

from typing import List
from config import settings
from schemas import SummaryResume
from services.base_resume_matcher import BaseResumeMatcher

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class OllamaResumeMatcher(BaseResumeMatcher):
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def _get_embedding(self, text: str) -> List[float]:
        response = requests.post(f"{settings.AI_SERVICE_KEY}/embed", json={
            "model": "bge-m3",
            "input": text
        })
        return response.json()['embeddings'][0]

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
                        "description": "Nome completo do candidato"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Um resumo completo e detalhado, incluindo formação acadêmica, principais experiências profissionais, competências e habilidades."
                    }
                },
                "required": [
                    "candidate_name",
                    "summary"
                ]
            }
        })
        return SummaryResume(**json.loads(response.json()['message']['content']))

    def rank_resumes_by_similarity(self, query: str, resumes: List[SummaryResume], k: int = 3, threshold: float = 0.5) -> List[SummaryResume]:
        scored_resumes = []
        query_embedding = self._get_embedding(query)

        for resume in resumes:

            resume_embedding = self._get_embedding(resume.summary)

            similarity = self._cosine_similarity(
                query_embedding, resume_embedding)

            if similarity >= threshold:
                scored_resumes.append((resume, similarity))

        scored_resumes.sort(key=lambda x: x[1], reverse=True)

        top_k = [resume for resume, _ in scored_resumes[:k]]
        logger.info(f'{scored_resumes}')
        return top_k

    def generate_candidate_justification(self, query: str, resumes: List[SummaryResume]) -> str:
        summaries = chr(10).join(
            [f"{i+1}. Nome: {r.candidate_name}\nResumo: {r.summary}" for i, r in enumerate(resumes)])

        prompt = f"""
        Você é uma especialista em análise de currículos com foco em identificar o candidato mais adequado com base em uma necessidade específica.

        A seguir está a descrição da vaga ou necessidade:
        ---
        {query}
        ---

        Com base nessa necessidade, analise detalhadamente os seguintes currículos, extraídos previamente e já resumidos:

        Resumos:
        {summaries}

        Tarefa:
        1. Avalie cada candidato em relação aos requisitos e contexto da vaga.
        2. Identifique o candidato que mais se adequa à descrição fornecida.
        3. Justifique sua escolha com base nas experiências, habilidades ou formação descritas no resumo.
        4. Seja claro, objetivo e completo na justificativa.

        Formato da resposta:
        - Candidato mais adequado: <Nome>
        - Justificativa: <Texto detalhado explicando por que este candidato é o mais adequado em comparação aos demais>
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
