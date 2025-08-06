from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar
from typing import Generic, TypeVar, List, Optional

TModel = TypeVar("TModel")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")
TID = TypeVar("TID")
T = TypeVar("T")


@dataclass
class PaginatedResult(Generic[T]):
    total: int
    skip: int
    limit: int
    data: List[T]


class CRUDRepository(ABC, Generic[TModel, TCreate, TUpdate, TID]):
    @abstractmethod
    def create(self, obj_in: TCreate) -> TModel:
        pass

    @abstractmethod
    def find_one(self, id: TID) -> Optional[TModel]:
        pass

    @abstractmethod
    def find_all(self) -> List[TModel]:
        pass

    @abstractmethod
    def find_all_paginated(
        self,
        skip: int = 0,
        limit: int = 10
    ) -> PaginatedResult[TModel]:
        pass

    @abstractmethod
    def update(self, id: TID, obj_in: TUpdate) -> TModel:
        pass

    @abstractmethod
    def delete(self, id: TID) -> None:
        pass
