from typing import List
from pydantic import BaseModel, Field


class AnalysisOutput(BaseModel):
    best_candidate: str = Field(...,
                                description="Nome ou identificador do melhor candidato")
    summaries: List[str] = Field(
        ..., description="Lista de resumos/sumários dos currículos enviados")
    justification: str = Field(
        ..., description="Justificativa de por que esse candidato foi o melhor")
    best_fit_score: float = Field(..., ge=0, le=1,
                                  description="Score de compatibilidade (0.0 a 1.0)")

    class Config:
        json_schema_extra = {
            "example": {
                "best_candidate": "Maria Silva",
                "summaries": [
                    "Maria Silva tem 5 anos de experiência em engenharia de software.",
                    "João Souza atuou como desenvolvedor backend por 2 anos."
                ],
                "justification": "Maria apresentou maior aderência à query: 'engenheiro com experiência em Python e liderança'.",
                "best_fit_score": 0.93
            }
        }
