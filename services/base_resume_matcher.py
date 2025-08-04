from typing import List
from schemas import SummaryResume
from abc import ABC, abstractmethod


class BaseResumeMatcher(ABC):
    @abstractmethod
    def extract_summary_from_resume(self, content: str) -> SummaryResume:
        """Extrai o nome do candidato e o resumo do currículo"""

    @abstractmethod
    def rank_resumes_by_similarity(self, query: str, resumes: List[SummaryResume], k: int, threshold: float) -> List[SummaryResume]:
        """Ordena os currículos por similaridade com a query."""

    @abstractmethod
    def generate_candidate_justification(self, query: str, resumes: List[SummaryResume]) -> str:
        """Gera uma justificativa textual usando os currículos mais relevantes."""
