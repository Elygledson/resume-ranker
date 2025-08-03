from bson import ObjectId
from models import LogModel
from typing import Optional, List
from schemas import LogCreateSchema, LogUpdateSchema
from repositories.base_repository import CRUDRepository


class LogRepositoryMongo(CRUDRepository[LogModel, LogCreateSchema, LogUpdateSchema, str]):
    def __init__(self, collection):
        self.collection = collection

    def create(self, obj_in: LogCreateSchema) -> LogModel:
        result = self.collection.insert_one(obj_in.model_dump())
        obj = self.collection.find_one({"_id": result.inserted_id})
        return LogModel(**obj)

    def find_one(self, id: str) -> Optional[LogModel]:
        doc = self.collection.find_one({"_id": ObjectId(id)})
        return LogModel(**doc) if doc else None

    def find_all(self) -> List[LogModel]:
        cursor = self.collection.find({})
        return [LogModel(**doc) for doc in cursor]

    def update(self, id: str, obj_in: LogUpdateSchema) -> LogModel:
        self.collection.update_one({"_id": ObjectId(id)}, {
            "$set": obj_in.model_dump(exclude_unset=True)})
        updated = self.collection.find_one({"_id": ObjectId(id)})
        return LogModel(**updated)

    def delete(self, id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(id)})
