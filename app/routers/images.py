from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..schemas import ErrorResponse, SuccessResponse
from ..database import get_db
from ..models import ProcessedImage
from ..s3 import s3_bucket_service_factory
from ..config import settings

router = APIRouter()
s3 = s3_bucket_service_factory(settings)


@router.post("/reorder")
async def reorder_images(image_ids: List[int], db: Session = Depends(get_db)):
    try:
        for index, image_id in enumerate(image_ids):
            db.query(ProcessedImage).filter(ProcessedImage.id == image_id).update(
                {"order": index}
            )
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=SuccessResponse(
                message="Images reordered successfully"
            ).model_dump(),
        )
    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Error reordering images", details=str(e)
            ).model_dump(),
        )


@router.delete("/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    try:
        # Get the image from the database
        image = db.query(ProcessedImage).filter(
            ProcessedImage.id == image_id).first()
        if not image:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResponse(
                    message="Image not found"
                ).model_dump()
            )

        # Delete the image from S3
        s3.delete_object(image.s3_filename)

        # Delete the image from the database
        db.delete(image)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=SuccessResponse(
                message="Image deleted successfully"
            ).model_dump()
        )
    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Error deleting image from database",
                details=str(e)
            ).model_dump()
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Error deleting image from S3",
                details=str(e)
            ).model_dump()
        )
