import io
from fastapi import APIRouter

import uuid
from pathlib import Path
from fastapi import File, UploadFile, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from PIL import Image


from .. import models, schemas
from ..database import get_db
from ..config import settings
from ..s3 import s3_bucket_service_factory

router = APIRouter()

s3 = s3_bucket_service_factory(settings)


@router.post("/edit/add-frame/", response_model=schemas.ImageResponse)
def process_image_json(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    frame_name: str = "frame.png"
) -> dict:
    """
    Принимает файл, растягивает рамку под его размер и возвращает JSON.
    """
    frame_path = Path("frames") / frame_name
    if not frame_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Frame '{frame_name}' not found."
        )

    try:

        # 1. Открываем оба изображения
        frame_image = Image.open(frame_path).convert("RGBA")
        user_image = Image.open(file.file).convert("RGBA")

        # 2. Растягиваем рамку до размера загруженного изображения
        frame_image = frame_image.resize(user_image.size)

        # 3. Создаем пустое изображение размером с оригинал
        combined = Image.new("RGBA", user_image.size)

        # 4. Накладываем сначала оригинальное изображение
        combined.paste(user_image, (0, 0))

        # 5. Сверху накладываем растянутую рамку, используя ее альфа-канал как маску
        combined.paste(frame_image, (0, 0), mask=frame_image)

        final_image = combined.convert("RGB")

        unique_id = uuid.uuid4()
        saved_filename = f"{unique_id}.jpg"
        save_path = Path("static/processed") / saved_filename

        # создается баффер
        img_byte_arr = io.BytesIO()

        # pil сохраняет в баффер
        final_image.save(img_byte_arr, "jpeg")

        # получаю значение
        img_byte_arr = img_byte_arr.getvalue()

        # формирую ссылку на картинку
        result_url = f"{settings.S3_PUBLIC_URL}/{saved_filename}"

        # делаю upload в s3
        s3.upload_object(saved_filename, img_byte_arr)

        # создаю экземпляр модели
        db_image = models.ProcessedImage(
            original_filename=file.filename,
            processed_url=result_url
        )

        # заменить на методы класса
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return {"filename": file.filename, "url": result_url}

    except Image.DecompressionBombError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size is too large."
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"An error occurred during processing: {e}"}
        )
