import enum

from datetime import datetime, timezone
from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, Field
from schemas.analysis_schemas import AnalysisOutputSchema


PyObjectId = Annotated[str, BeforeValidator(str)]


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
    result: Optional[AnalysisOutputSchema] = Field(
        None, description="Resposta gerada pela aplicação"
    )
    feedback: Optional[bool] = Field(
        None, description="Feedback do usuário (True = gostei, False = não gostei)"
    )

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "request_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                "timestamp": "2025-08-02T14:00:00Z",
                "query": "engenheiro com experiência em Python e liderança",
                "status": "PROCESSED",
                "result": {
                    "resumes": [
                        {
                            "candidate_name": "Maria Silva",
                            "summary": "Engenheira de software com 5 anos de experiência em Python e liderança de equipes.",
                            "score": 0.8,
                        },
                        {
                            "candidate_name": "João Souza",
                            "summary": "Desenvolvedor backend com 2 anos de experiência em Java e Spring Boot.",
                            "score": 0.6,
                        }
                    ],
                    "justification": "Maria Silva apresentou maior aderência aos critérios de liderança e domínio em Python."
                }
            }
        }


class LogUpdateSchema(BaseModel):
    status: Optional[Status] = None
    result: Optional[AnalysisOutputSchema] = None
    feedback: Optional[bool] = None

    class Config:
        use_enum_values = True
        from_attributes = True


class LogOutputSchema(LogCreateSchema):
    id: str = Field(..., description="ID gerado para o log")

    class Config:
        from_attributes = True


class PaginatedLogsSchema(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[LogOutputSchema]

    class Config:
        json_schema_extra = {
            "example": {
                "total": 150,
                "skip": 0,
                "limit": 10,
                "data": [
                    {
                        "id": "64c7f1f4a1c4c8e1c4e1d2a3",
                        "request_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                        "timestamp": "2025-08-02T14:00:00Z",
                        "query": "engenheiro com experiência em Python e liderança",
                        "status": "PROCESSED",
                        "result": {
                            "resumes": [
                                {
                                    "candidate_name": "Maria Silva",
                                    "summary": "Engenheira de software com 5 anos de experiência em Python e liderança de equipes.",
                                    "score": 0.8,
                                }
                            ],
                            "justification": "Maria Silva apresentou maior aderência aos critérios de liderança e domínio em Python."
                        },
                        "feedback": True
                    }
                ]
            }
        }
