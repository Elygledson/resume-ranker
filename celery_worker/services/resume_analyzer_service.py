from typing import List
from schemas import SummaryResume
from services.base_resume_matcher import BaseResumeMatcher


class ResumeAnalyzerService:
    def __init__(self, matcher: BaseResumeMatcher) -> None:
        self.llm_service = matcher

    def generate_summary(self, content: str) -> SummaryResume:
        return self.llm_service.extract_summary_from_resume(content)

    def rank_resumes(self, query: str, resumes: List[SummaryResume], k: int = 5, threshold: float = 0.5) -> List[SummaryResume]:
        return self.llm_service.rank_resumes_by_similarity(query, resumes, k, threshold)

    def generate_justification(self, query: str, resumes: List[SummaryResume]) -> str:
        return self.llm_service.generate_candidate_justification(query, resumes)
