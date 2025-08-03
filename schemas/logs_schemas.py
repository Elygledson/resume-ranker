import enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from schemas.analysis_schemas import AnalysisOutputSchema


class Status(enum.Enum):
    PROCESSING_FAILED = 'PROCESSING_FAILED'
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class LogCreateSchema(BaseModel):
    request_id: str = Field(..., description="ID único da requisição")
    user_id: str = Field(..., description="ID do usuário que fez a requisição")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Data e hora da requisição (formato ISO 8601, UTC)"
    )
    query: Optional[str] = Field(
        None, description="Consulta feita pelo usuário"
    )
    status: Status
    resultado: Optional[AnalysisOutputSchema] = Field(
        None, description="Resposta gerada pela aplicação"
    )

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "request_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "user_id": "1",
                "timestamp": "2025-08-02T14:00:00Z",
                "query": "engenheiro com experiência em Python e liderança",
                "status": "PROCESSED",
                "resultado": {
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
        }


class LogUpdateSchema(LogCreateSchema):
    id: str = Field(..., description="ID do log a ser atualizado")


class LogOutputSchema(LogCreateSchema):
    id: str = Field(..., description="ID gerado para o log")
