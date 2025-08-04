from typing import List, Optional
from pydantic import BaseModel, Field


class ResumeAnalysisStartedResponse(BaseModel):
    log_id: str
    message: str = Field(
        default="Os currículos foram enviados para análises",
        description="Mensagem indicando que a análise foi iniciada com sucesso"
    )


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


class AnalysisOutputSchema(BaseModel):
    resumes: List[SummaryResume] = Field(
        ..., description="Lista dos currículos analisados"
    )
    justification: Optional[str] = Field(
        None, description="Justificativa para a seleção ou análise feita"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "resumes": [
                    {
                        "candidate_name": "Maria Silva",
                        "summary": "Engenheira de software com 5 anos de experiência em Python e liderança de equipes.",
                    },
                    {
                        "candidate_name": "João Souza",
                        "summary": "Desenvolvedor backend com 2 anos de experiência em Java e Spring Boot.",
                    }
                ],
                "justification": "Maria Silva apresentou maior aderência aos critérios de liderança e domínio em Python."
            }
        }
