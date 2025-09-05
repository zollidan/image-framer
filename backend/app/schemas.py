"""
Pydantic schemas for the application.

This module defines the Pydantic models used for data validation and
serialization in the API requests and responses.
"""
import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class ImageResponse(BaseModel):
    """
    Schema for the response containing image information.

    Attributes:
        filename (str): The name of the image file.
        url (str): The URL to access the image.
    """
    filename: str
    url: str

    class Config:
        orm_mode = True


class SuccessResponse(BaseModel):
    """
    Generic schema for a successful API response.

    Attributes:
        success (bool): Indicates if the request was successful.
        message (str): A message describing the result.
        data (Optional[dict]): Additional data to be returned.
        timestamp (Optional[str]): The timestamp of the response.
        request_id (Optional[str]): A unique identifier for the request.
    """
    success: bool = True
    message: str
    data: Optional[dict] = None
    timestamp: Optional[str] = datetime.datetime.now().isoformat()
    request_id: Optional[str] = str(uuid.uuid4())


class ErrorResponse(BaseModel):
    """
    Generic schema for an error API response.

    Attributes:
        success (bool): Indicates that the request failed.
        message (str): A summary of the error.
        details (Optional[str]): Detailed information about the error.
        error_code (Optional[str]): A specific error code.
        timestamp (Optional[str]): The timestamp of the response.
        request_id (Optional[str]): A unique identifier for the request.
    """
    success: bool = False
    message: str
    details: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: Optional[str] = datetime.datetime.now().isoformat()
    request_id: Optional[str] = str(uuid.uuid4())
