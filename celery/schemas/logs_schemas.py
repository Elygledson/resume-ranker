import enum

from typing import Optional
from pydantic import BaseModel
from schemas.analysis_schemas import AnalysisOutputSchema


class Status(enum.Enum):
    PROCESSING_FAILED = 'PROCESSING_FAILED'
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class LogUpdateSchema(BaseModel):
    status: Optional[Status] = None
    resultado: Optional[AnalysisOutputSchema] = None
    feedback: Optional[bool] = None

    class Config:
        use_enum_values = True
