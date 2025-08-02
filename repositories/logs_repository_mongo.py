from bson import ObjectId
from models import LogModel
from typing import Optional, List
from repositories.base_repository import CRUDRepository
from schemas.logs_schemas import LogCreateSchema, LogUpdateSchema


class LogRepositoryMongo(CRUDRepository[LogModel, LogCreateSchema, LogUpdateSchema, str]):
    def __init__(self, collection):
        self.collection = collection

    async def create(self, obj_in: LogCreateSchema) -> LogModel:
        result = await self.collection.insert_one(obj_in.model_dump())
        obj = await self.collection.find_one({"_id": result.inserted_id})
        return LogModel(**obj)

    async def find_one(self, id: str) -> Optional[LogModel]:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        return LogModel(**doc) if doc else None

    async def find_all(self) -> List[LogModel]:
        cursor = self.collection.find({})
        return [LogModel(**doc) async for doc in cursor]

    async def update(self, id: str, obj_in: LogUpdateSchema) -> LogModel:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": obj_in.model_dump(exclude_unset=True)})
        updated = await self.collection.find_one({"_id": id})
        return LogModel(**updated)

    async def delete(self, id: str) -> None:
        await self.collection.delete_one({"_id": ObjectId(id)})
