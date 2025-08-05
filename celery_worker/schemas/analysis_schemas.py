from typing import Optional
from pydantic import BaseModel, Field


class SummaryResume(BaseModel):
    candidate_name: str = Field(..., description="Nome do candidato")
    summary: str = Field(..., description="Resumo extraído do currículo")
    score: Optional[float] = Field(
        default=0,
        description="Pontuação de similaridade do candidato com a vaga"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "candidate_name": "Maria Silva",
                "summary": "Engenheira de software com 5 anos de experiência em Python e liderança de equipes.",
                "score": 0.6
            }
        }
