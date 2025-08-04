from services.base_resume_matcher import BaseResumeMatcher
from services.ollama_resume_matcher import OllamaResumeMatcher


def get_matcher(strategy: str = "ollama") -> BaseResumeMatcher:
    if strategy == "ollama":
        return OllamaResumeMatcher()
    elif strategy == "gemini":
        pass
    raise ValueError(f"Estratégia não suportada: {strategy}")
