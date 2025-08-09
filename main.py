# main.py
import uuid
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from PIL import Image

# Импортируем наши модули
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="InstaRetro App")

# --- Настройка статических файлов и шаблонов ---
Path("static/processed").mkdir(parents=True, exist_ok=True)
Path("frames").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Логика работы с БД (без изменений) ---


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- РОУТ для отображения HTML-интерфейса (без изменений) ---


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --- ОБНОВЛЕННЫЙ JSON-ЭНДПОИНТ для обработки ---
@app.post("/process-json/", response_model=schemas.ImageResponse)
def process_image_json(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    frame_name: str = "frame.png"  # <-- ИЗМЕНЕНИЕ: Файл рамки по умолчанию
):
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
        # --- ИЗМЕНЕНА ЛОГИКА ОБРАБОТКИ ---

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

        # --- КОНЕЦ ИЗМЕНЕНИЙ В ЛОГИКЕ ---

        final_image = combined.convert("RGB")

        unique_id = uuid.uuid4()
        saved_filename = f"{unique_id}.jpg"
        save_path = Path("static/processed") / saved_filename
        final_image.save(save_path, "jpeg")

        result_url = f"/static/processed/{saved_filename}"

        db_image = models.ProcessedImage(
            original_filename=file.filename,
            processed_url=result_url
        )
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
