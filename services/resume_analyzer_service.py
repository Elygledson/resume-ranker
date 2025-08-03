from typing import List
from schemas import SummaryResume
from services.base_resume_matcher import BaseResumeMatcher


class ResumeAnalyzerService:
    def __init__(self, matcher: BaseResumeMatcher) -> None:
        self.llm_service = matcher

    def generate_summary(self, content: str) -> SummaryResume:
        return self.llm_service.extract_summary_from_resume(content)

    def find_best_resume(self, query: str, resumes: List[SummaryResume]) -> str:
        return self.llm_service.find_best_match(query, resumes)
