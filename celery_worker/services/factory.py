import enum

from services.base_resume_matcher import BaseResumeMatcher
from services.gemini_resume_matcher import GeminiResumeMatcher
from services.ollama_resume_matcher import OllamaResumeMatcher


class ResumeMatcherStrategy(enum.Enum):
    OLLAMA = "ollama"
    GEMINI = "gemini"


def get_matcher(strategy: str = "ollama") -> BaseResumeMatcher:
    if strategy.lower() == ResumeMatcherStrategy.OLLAMA.value:
        return OllamaResumeMatcher()
    elif strategy.lower() == ResumeMatcherStrategy.GEMINI.value:
        return GeminiResumeMatcher()
    raise ValueError(f"Estratégia não suportada: {strategy}")
