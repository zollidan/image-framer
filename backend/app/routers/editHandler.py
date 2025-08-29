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


@router.post("/add-white-bg/", response_model=schemas.ImageResponse)
def process_add_white_bg(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    bg_coefficient: float = 1.3
):
    """
    Принимает файл изображения, накладывает его на белый фон
    и возвращает URL обработанного изображения.
    """

    try:
        # 1. Чтение файла и получение размеров из size: tuple[int, int]
        contents = file.file.read()
        user_image = Image.open(io.BytesIO(contents)).convert("RGBA")
        original_width, original_height = user_image.size

        # 2. Вычесление новых размеров для фона.
        new_width = int(original_width * bg_coefficient)
        new_height = int(original_height * bg_coefficient)

        # 3. Создание фонового изображения
        background = Image.new("RGBA", (new_width, new_height), "WHITE")

        # 4. Вычесление новых кардинат на вставку в центр белого фона
        paste_x = (new_width - original_width) // 2
        paste_y = (new_height - original_height) // 2

        # 5. Наложение по центру на белый фон
        background.paste(user_image, (paste_x, paste_y), user_image)

        # 6. Финальное конвертирование
        final_image = background.convert("RGB")

        unique_id = uuid.uuid4()
        saved_filename = f"{unique_id}.jpg"

        img_byte_arr = io.BytesIO()

        final_image.save(img_byte_arr, format='JPEG')

        img_byte_arr = img_byte_arr.getvalue()

        result_url = f"{settings.S3_PUBLIC_URL}/{saved_filename}"

        s3.upload_object(saved_filename, img_byte_arr)

        db_image = models.ProcessedImage(
            original_filename=file.filename,
            processed_url=result_url
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return {"filename": file.filename, "url": result_url}

    except Image.DecompressionBombError:
        # Обработка ошибки, если изображение слишком большое
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size is too large."
        )
    except Exception as e:
        # Обработка других возможных ошибок при обработке
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"An error occurred during processing: {e}"}
        )


@router.post("/add-frame/", response_model=schemas.ImageResponse)
def process_add_frame(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    frame_name: str = "frame.png",
    quality: int = 100  # Изменяем дефолт на 100 для максимального качества
) -> dict:
    """
    Принимает файл, растягивает рамку под его размер и возвращает JSON.
    Сохраняет оригинальное качество, разрешение, цветовую палитру и профили.
    """
    frame_path = Path("frames") / frame_name
    if not frame_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Frame '{frame_name}' not found."
        )

    try:
        # 1. Открываем оба изображения с сохранением профилей и метаданных
        frame_image = Image.open(frame_path)
        user_image = Image.open(file.file)

        # Сохраняем оригинальные свойства
        original_size = user_image.size  # Разрешение уже сохраняется, но фиксируем
        original_icc_profile = user_image.info.get('icc_profile')
        original_exif = user_image.info.get('exif')
        original_mode = user_image.mode
        original_palette = user_image.getpalette() if original_mode == 'P' else None
        original_format = user_image.format or 'JPEG'

        # 2. Конвертируем в RGBA только для композита, если необходимо
        user_rgba = user_image.convert(
            "RGBA") if user_image.mode != "RGBA" else user_image
        frame_rgba = frame_image.convert(
            "RGBA") if frame_image.mode != "RGBA" else frame_image

        # 3. Растягиваем рамку с высококачественным ресемплингом, сохраняя оригинальное разрешение
        frame_rgba = frame_rgba.resize(
            original_size,
            resample=Image.Resampling.LANCZOS  # Высококачественный алгоритм
        )

        # 4. Создаем композитное изображение в RGBA
        combined = Image.alpha_composite(user_rgba, frame_rgba)

        # 5. Восстанавливаем оригинальный режим после композита
        if original_mode == 'P':
            # Для палитры: пытаемся квантизовать обратно, сохраняя цвета
            if original_palette:
                combined = combined.quantize(
                    colors=256, method=2, palette=Image.ADAPTIVE)
                # Если есть оригинальная палитра, применяем её
                combined.putpalette(original_palette)
            else:
                combined = combined.quantize(colors=256)
        elif original_mode == 'L':
            # Для grayscale конвертируем обратно
            combined = combined.convert('L')
        elif original_mode == 'CMYK':
            # Для CMYK: конвертируем обратно после композита
            combined = combined.convert('CMYK')
        elif original_mode == 'RGB':
            combined = combined.convert('RGB')
        elif original_mode == 'RGBA':
            # Оставляем как есть
            pass
        else:
            # По умолчанию RGB для других режимов
            combined = combined.convert('RGB')

        # 6. Восстанавливаем цветовой профиль
        if original_icc_profile:
            combined.info['icc_profile'] = original_icc_profile

        unique_id = uuid.uuid4()
        saved_filename = f"{unique_id}.jpg"

        # 7. Определяем формат сохранения с приоритетом на lossless
        if original_format.upper() in ['PNG', 'WEBP', 'GIF']:
            # Для lossless форматов используем lossless сохранение
            if original_format.upper() == 'PNG':
                saved_filename = f"{unique_id}.png"
                save_format = "PNG"
                save_kwargs = {
                    'optimize': True,
                    'compress_level': 1  # Минимальная компрессия для максимального качества
                }
            elif original_format.upper() == 'WEBP':
                saved_filename = f"{unique_id}.webp"
                save_format = "WEBP"
                save_kwargs = {
                    'lossless': True,
                    'quality': 100,
                    'method': 6  # Максимальное качество
                }
            else:  # GIF или другие, сохраняем как PNG
                saved_filename = f"{unique_id}.png"
                save_format = "PNG"
                save_kwargs = {
                    'optimize': True,
                    'compress_level': 1
                }
        else:
            # Для JPEG и других используем максимальное качество
            saved_filename = f"{unique_id}.jpg"
            save_format = "JPEG"
            save_kwargs = {
                'quality': quality if quality <= 100 else 100,
                'optimize': False,  # Отключаем оптимизацию для сохранения качества
                'progressive': True,
                'subsampling': 0,  # 4:4:4 для максимального качества
                'qtables': 'web_high'
            }

        # Добавляем EXIF если был и формат поддерживает
        if original_exif and save_format in ["JPEG", "PNG", "WEBP"]:
            save_kwargs['exif'] = original_exif

        # 8. Создаем буфер и сохраняем с настройками максимального качества
        img_byte_arr = io.BytesIO()
        combined.save(img_byte_arr, save_format, **save_kwargs)
        img_byte_arr = img_byte_arr.getvalue()

        # 9. Формируем ссылку и загружаем в S3
        result_url = f"{settings.S3_PUBLIC_URL}/{saved_filename}"
        s3.upload_object(saved_filename, img_byte_arr)

        # 10. Сохраняем в БД
        db_image = models.ProcessedImage(
            original_filename=file.filename,
            processed_url=result_url
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return {
            "filename": file.filename,
            "url": result_url,
            "quality": quality,
            "format": save_format
        }

    except Image.DecompressionBombError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size is too large."
        )
    except Exception as e:
        # logger.error(f"Error processing image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"An error occurred during processing: {e}"}
        )
