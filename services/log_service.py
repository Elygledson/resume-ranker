from bson import ObjectId
from models import LogModel
from typing import List, Optional
from repositories import CRUDRepository
from fastapi import HTTPException, status
from schemas import LogCreateSchema, LogUpdateSchema


class LogService:
    def __init__(self, repo: CRUDRepository[LogModel, LogCreateSchema, LogUpdateSchema, str]):
        self.repo = repo

    async def create(self, data: LogCreateSchema) -> LogModel:
        return await self.repo.create(data)

    async def get(self, id: str) -> Optional[LogModel]:
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID inválido"
            )

        log = await self.repo.find_one(id)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Log não encontrado"
            )

        return log

    async def get_all(self) -> List[LogModel]:
        return await self.repo.find_all()

    async def update(self, id: str, data: LogUpdateSchema) -> LogUpdateSchema:
        return await self.repo.update(id, data)

    async def delete(self, id: str) -> None:
        log = await self.get(id)
        await self.repo.delete(log.id)
