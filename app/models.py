# models.py
from sqlalchemy import Column, Integer, String
from .database import Base


from sqlalchemy import Column, DateTime, Integer, String, func


class ProcessedImage(Base):
    __tablename__ = "processed_images"

    id = Column(Integer, primary_key=True)
    original_filename = Column(String, nullable=False)
    s3_filename = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    order = Column(Integer, default=0)
