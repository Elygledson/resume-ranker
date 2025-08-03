from bson import ObjectId
from datetime import datetime
from typing import Annotated, Optional
from schemas import AnalysisOutputSchema, Status
from pydantic import BaseModel, Field, BeforeValidator


PyObjectId = Annotated[str, BeforeValidator(str)]


class LogModel(BaseModel):
    id: PyObjectId = Field(alias="_id")
    request_id: str
    user_id: str
    timestamp: datetime
    query: Optional[str] = None
    status: Status
    resultado: Optional[AnalysisOutputSchema] = None
    feedback: Optional[bool] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
