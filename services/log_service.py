from bson import ObjectId
from models import LogModel
from typing import List, Optional
from repositories import CRUDRepository
from fastapi import HTTPException, status
from schemas import LogCreateSchema, LogUpdateSchema


class LogService:
    def __init__(self, repo: CRUDRepository[LogModel, LogCreateSchema, LogUpdateSchema, str]):
        self.repo = repo

    def create(self, data: LogCreateSchema) -> LogModel:
        return self.repo.create(data)

    def get(self, id: str) -> Optional[LogModel]:
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

        return log

    def get_all(self) -> List[LogModel]:
        return self.repo.find_all()

    def update(self, id: str, data: LogUpdateSchema) -> LogUpdateSchema:
        log = self.get(id)
        return self.repo.update(log.id, data)

    def patch_feedback(self, id: str, feedback: bool) -> LogUpdateSchema:
        log = self.get(id)
        return self.repo.update(log.id, LogUpdateSchema(feedback=feedback))

    def delete(self, id: str) -> None:
        log = self.get(id)
        self.repo.delete(log.id)
