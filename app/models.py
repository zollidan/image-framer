# models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class ProcessedImage(Base):
    __tablename__ = "processed_images"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String)
    processed_url = Column(String, unique=True)