import io
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from PIL import Image

from .. import models, schemas
from ..config import settings
from ..database import get_db
from ..s3 import s3_bucket_service_factory

router = APIRouter()

# Create a single S3 service instance for reuse.
s3 = s3_bucket_service_factory(settings)


@router.post("/add-white-bg/", response_model=schemas.ImageResponse)
def process_add_white_bg(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    bg_coefficient: float = 1.3,
) -> dict:
    """Place the uploaded image on a white background and return its URL."""
    try:
        contents = file.file.read()
        user_image = Image.open(io.BytesIO(contents)).convert("RGBA")
        new_width = int(user_image.width * bg_coefficient)
        new_height = int(user_image.height * bg_coefficient)
        background = Image.new("RGBA", (new_width, new_height), "WHITE")
        paste_x = (new_width - user_image.width) // 2
        paste_y = (new_height - user_image.height) // 2
        background.paste(user_image, (paste_x, paste_y), user_image)
        final_image = background.convert("RGB")

        unique_id = uuid.uuid4()
        saved_filename = f"{unique_id}.jpg"
        buffer = io.BytesIO()
        final_image.save(buffer, format="JPEG")
        s3.upload_object(saved_filename, buffer.getvalue())
        result_url = f"{settings.S3_PUBLIC_URL}/{saved_filename}"

        db_image = models.ProcessedImage(
            original_filename=file.filename,
            processed_url=result_url,
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return {"filename": file.filename, "url": result_url}
    except Image.DecompressionBombError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size is too large.",
        )
    except Exception as e:  # pragma: no cover - defensive programming
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during processing: {e}",
        )


@router.post("/add-frame/", response_model=schemas.ImageResponse)
def process_add_frame(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    frame_name: str = "frame.png",
) -> dict:
    """Overlay the uploaded image with a frame and return its URL."""
    frame_path = Path("frames") / frame_name
    if not frame_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Frame '{frame_name}' not found.",
        )

    try:
        user_image = Image.open(file.file).convert("RGBA")
        frame_image = Image.open(frame_path).convert("RGBA")
        frame_image = frame_image.resize(user_image.size)
        combined = Image.alpha_composite(user_image, frame_image).convert("RGB")

        unique_id = uuid.uuid4()
        saved_filename = f"{unique_id}.jpg"
        buffer = io.BytesIO()
        combined.save(buffer, format="JPEG")
        s3.upload_object(saved_filename, buffer.getvalue())
        result_url = f"{settings.S3_PUBLIC_URL}/{saved_filename}"

        db_image = models.ProcessedImage(
            original_filename=file.filename,
            processed_url=result_url,
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return {"filename": file.filename, "url": result_url}
    except Image.DecompressionBombError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size is too large.",
        )
    except Exception as e:  # pragma: no cover - defensive programming
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during processing: {e}",
        )
