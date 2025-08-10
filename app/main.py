# main.py
from pathlib import Path
from fastapi import FastAPI


from . import models
from .database import engine
from .routers import s3Handler
from .routers import editHandler
from .routers import dbHandler

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="InstaRetro App")

# --- Routers
app.include_router(s3Handler.router)
app.include_router(editHandler.router)
app.include_router(dbHandler.router)

# --- Настройка статических файлов и шаблонов ---
Path("static/processed").mkdir(parents=True, exist_ok=True)
Path("frames").mkdir(exist_ok=True)
