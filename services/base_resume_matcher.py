from typing import List
from schemas import SummaryResume
from abc import ABC, abstractmethod


class BaseResumeMatcher(ABC):
    @abstractmethod
    def extract_summary_from_resume(self, content: str) -> SummaryResume:
        pass

    @abstractmethod
    def find_best_match(self, query: str, resumes: List[SummaryResume]) -> str:
        pass

    @abstractmethod
    def generate_best_match(self, query: str, resumes: List[SummaryResume]) -> str:
        pass


