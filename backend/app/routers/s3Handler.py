import os
from typing import Annotated
import uuid
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse

from ..s3 import s3_bucket_service_factory
from ..config import settings
from ..schemas import *

router = APIRouter()

s3 = s3_bucket_service_factory(settings)

@router.get("/list")
def get_list_objects() -> list[str]:
    return s3.list_objects()


@router.get("/file/{file_key}")
async def get_file_by_key(file_key: str):

    try:
        file = s3.get_object_by_key(file_key)

        return StreamingResponse(content=file['Body'])
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Error download file!",
                details=str(e)
            ).model_dump()
        )


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: Annotated[UploadFile, File()]) -> dict:

    try:

        file_content = await file.read()

        # Валидация размера файла
        if len(file_content) > settings.MAX_FILE_SIZE:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ErrorResponse(
                    message="File is too large!").model_dump()
            )

        # Валидация типа файла
        if file.content_type not in settings.ALLOWED_TYPES:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ErrorResponse(
                    message="File type is unknown!").model_dump()
            )

        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        s3.upload_object(unique_filename, file_content)

        return JSONResponse(content=SuccessResponse(
            message="File uploaded successfully",
            data={
                "original_filename": file.filename,
                "s3_filename": unique_filename,
                "size": len(file_content),
                "content_type": file.content_type,
            }
        ).model_dump())

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Error uploading file!", details=str(e))
        )
    finally:
        await file.close()
