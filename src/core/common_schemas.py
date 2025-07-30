from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    model_config = {
        "extra": "forbid",
        "from_attributes": True
    }

class ResponseModel(BaseModel):
    method: str
    timestamp: datetime = Field(default_factory= lambda : datetime.now(timezone.utc))
    path: str
    message: str = Field(default="Success")
    status_code: int = Field(default=200)
    data: Any

class ErrorModel(BaseModel):
    method: str
    timestamp: datetime = Field(default_factory= lambda : datetime.now(timezone.utc))
    path: str
    error: str | list
    status_code: int