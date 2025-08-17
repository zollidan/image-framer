# main.py
import os
from pathlib import Path
from app.s3 import s3_bucket_service_factory
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


from . import models
from .config import settings
from .database import engine
from .routers import s3Handler
from .routers import dbHandler
from .routers import images

models.Base.metadata.create_all(bind=engine)

s3 = s3_bucket_service_factory(settings)
s3.create_bucket()

# --- Настройка статических файлов и шаблонов ---
Path("static/assets").mkdir(parents=True, exist_ok=True)
Path("frames").mkdir(exist_ok=True)

app = FastAPI(title="InstaRetro App")

app.mount(
    "/assets",
    StaticFiles(directory="static/assets"),
    name="assets"
)


# --- Routers
app.include_router(s3Handler.router, prefix="/s3")
app.include_router(dbHandler.router, prefix="/files")
app.include_router(images.router, prefix="/images", tags=["images"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- React static


@app.get("/{full_path:path}")
async def serve_react_app(request: Request, full_path: str):
    index_path = "static/index.html"
    if not os.path.exists(index_path):
        return {"error": "index.html not found"}, 404
    return FileResponse(index_path)
