import logging
import numpy as np

from typing import List
from google import genai
from config import settings
from google.genai import types
from schemas import SummaryResume
from services.base_resume_matcher import BaseResumeMatcher

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GeminiResumeMatcher(BaseResumeMatcher):
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.AI_SERVICE_KEY)

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def _get_embedding(self, text: str) -> List[float]:
        return self.client.models.embed_content(model="text-embedding-004", contents=text).embeddings[0].values

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

        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                'response_schema': {
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
                    "required": ["candidate_name", "summary"]
                }
            },
        )
        return SummaryResume(**response.parsed)

    def rank_resumes_by_similarity(self, query: str, resumes: List[SummaryResume], k: int = 5, threshold: float = 0.5) -> List[SummaryResume]:
        scored_resumes: List[SummaryResume] = []
        query_embedding = self._get_embedding(query)

        for resume in resumes:

            resume_embedding = self._get_embedding(resume.summary)

            similarity = self._cosine_similarity(
                query_embedding, resume_embedding)

            if similarity >= threshold:
                resume.score = similarity
                scored_resumes.append(resume)

        scored_resumes.sort(key=lambda x: x.score or 0, reverse=True)
        top_k = scored_resumes[:k]

        logger.info(
            f"Top {len(top_k)} currículos selecionados (threshold={threshold}, k={k}): "
            + ", ".join(f"{r.candidate_name} ({r.score}%)" for r in top_k)
        )

        return top_k

    def generate_candidate_justification(self, query: str, resumes: List[SummaryResume]) -> str:
        summaries = chr(10).join(
            [f"{i+1}. Nome: {r.candidate_name}\nResumo: {r.summary}" for i, r in enumerate(resumes)])

        contents = f"""
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
        logger.info(f'{contents}')
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction="Você é uma especialista em análise de currículos com foco em identificar o"
                "candidato mais adequado com base em uma necessidade específica.",
            ),
        )
        return response.text
