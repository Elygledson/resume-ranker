from bson import ObjectId
from models import LogModel
from pydantic import TypeAdapter
from typing import List, Optional
from fastapi import HTTPException, status
from repositories import CRUDRepository, PaginatedResult
from schemas import LogCreateSchema, LogUpdateSchema, PaginatedLogsSchema, LogOutputSchema


class LogService:
    def __init__(self, repo: CRUDRepository[LogModel, LogCreateSchema, LogUpdateSchema, str]):
        self.repo = repo

    def create(self, data: LogCreateSchema) -> LogOutputSchema:
        log = self.repo.create(data)
        return LogOutputSchema.model_validate(log)

    def get(self, id: str) -> Optional[LogOutputSchema]:
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID inválido"
            )

        log = self.repo.find_one(id)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Log não encontrado"
            )

        return LogOutputSchema.model_validate(log)

    def get_all(self) -> List[LogOutputSchema]:
        logs = self.repo.find_all()
        return TypeAdapter(list[LogOutputSchema]).validate_python(logs)

    def get_all_paginated(self, skip: int = 0, limit: int = 10) -> PaginatedLogsSchema:
        paginated: PaginatedResult[LogModel] = self.repo.find_all_paginated(
            skip, limit)
        return PaginatedLogsSchema.model_validate(paginated)

    def update(self, id: str, data: LogUpdateSchema) -> LogOutputSchema:
        log = self.get(id)
        updated_log = self.repo.update(log.id, data)
        return LogOutputSchema.model_validate(updated_log)

    def patch_feedback(self, id: str, feedback: bool) -> LogOutputSchema:
        log = self.get(id)
        updated_log = self.repo.update(
            log.id, LogUpdateSchema(feedback=feedback))
        return LogOutputSchema.model_validate(updated_log)

    def delete(self, id: str) -> None:
        log = self.get(id)
        self.repo.delete(log.id)
