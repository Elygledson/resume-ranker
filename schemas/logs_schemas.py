from datetime import datetime
from pydantic import BaseModel, Field


class LogCreateSchema(BaseModel):
    request_id: str = Field(..., description="ID único da requisição")
    user_id: str = Field(..., description="ID do usuário que fez a requisição")
    timestamp: datetime = Field(...,
                                description="Data e hora da requisição (formato ISO 8601)")
    query: str = Field(..., description="Consulta feita pelo usuário")
    resultado: str = Field(..., description="Resposta gerada pela aplicação")

    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_123456",
                "user_id": "user_abc",
                "timestamp": "2025-08-02T14:00:00Z",
                "query": "Qual é o capital da França?",
                "resultado": "Paris"
            }
        }


class LogUpdateSchema(LogCreateSchema):
    id: str = Field(..., description="ID do log a ser atualizado")


class LogOutputSchema(LogCreateSchema):
    id: str = Field(..., description="ID gerado para o log")
