from pydantic import BaseModel, Field


class SummaryResume(BaseModel):
    candidate_name: str = Field(..., description="Nome do candidato")
    summary: str = Field(..., description="Resumo extraído do currículo")

    class Config:
        json_schema_extra = {
            "example": {
                "candidate_name": "Maria Silva",
                "summary": "Engenheira de software com 5 anos de experiência em Python e liderança de equipes.",
            }
        }
