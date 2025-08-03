from schemas import SummaryResume
from services import OllamaService


class ResumeAnalyzerService:
    def __init__(self) -> None:
        self.llm_service = OllamaService()

    def generate_summary(self, content: str) -> SummaryResume:
        return self.llm_service.extract_summary_from_resume(content)

    def find_best_resume(self, query: str, resumes: list[SummaryResume]) -> str:
        return self.llm_service.find_best_match(query, resumes)
