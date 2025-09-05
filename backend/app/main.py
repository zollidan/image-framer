# main.py
"""
Main application file for the FastAPI backend.

This file initializes the FastAPI application, sets up CORS middleware,
and includes the routers for different API endpoints.
"""
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
from .routers import editHandler
from .routers import dbHandler

models.Base.metadata.create_all(bind=engine)
# --- Настройка статических файлов и шаблонов ---
Path("frames").mkdir(exist_ok=True)

app = FastAPI(
    title="alice.com API",   
    root_path="/api",                
    root_path_in_servers=True,        
    docs_url="/docs",                 
    redoc_url="/redoc",             
    openapi_url="/openapi.json",  )

# --- Routers
app.include_router(s3Handler.router, prefix="/s3")
app.include_router(editHandler.router, prefix="/edit")
app.include_router(dbHandler.router, prefix="/files")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
