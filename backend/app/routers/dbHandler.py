"""
API router for database-related operations.

This module defines the API endpoints for listing processed images
stored in the database.
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..schemas import ErrorResponse

from ..database import get_db
from ..models import ProcessedImage

router = APIRouter()


@router.get("/list")
async def get_db_image_files(
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all processed images from the database.

    Args:
        db (Session): The database session, injected by Depends(get_db).

    Returns:
        list[ProcessedImage]: A list of processed image records.
        JSONResponse: An error response if a database error occurs.
    """
    try:
        files = db.scalars(select(ProcessedImage)).all()
        return files
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Error",
                details=str(e)
            ).model_dump()
        )
