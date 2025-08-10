import datetime
from enum import Enum
from typing import Any, Dict, Optional
import uuid
from pydantic import BaseModel


class ImageResponse(BaseModel):
    filename: str
    url: str

    class Config:
        orm_mode = True


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None
    timestamp: Optional[str] = datetime.datetime.now().isoformat()
    request_id: Optional[str] = str(uuid.uuid4())


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: Optional[str] = datetime.datetime.now().isoformat()
    request_id: Optional[str] = str(uuid.uuid4())
