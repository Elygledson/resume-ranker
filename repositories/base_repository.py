from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

TModel = TypeVar("TModel")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")
TID = TypeVar("TID")


class CRUDRepository(ABC, Generic[TModel, TCreate, TUpdate, TID]):
    @abstractmethod
    async def create(self, obj_in: TCreate) -> TModel:
        pass

    @abstractmethod
    async def find_one(self, id: TID) -> Optional[TModel]:
        pass

    @abstractmethod
    async def find_all(self) -> List[TModel]:
        pass

    @abstractmethod
    async def update(self, id: TID, obj_in: TUpdate) -> TModel:
        pass

    @abstractmethod
    async def delete(self, id: TID) -> None:
        pass
