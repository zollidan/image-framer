# models.py
"""
SQLAlchemy models for the application.

This module defines the database schema using SQLAlchemy's declarative base.
"""
from sqlalchemy import Column, Integer, String
from .database import Base


class ProcessedImage(Base):
    """
    Represents a processed image in the database.

    Attributes:
        id (int): The primary key for the processed image.
        original_filename (str): The original filename of the uploaded image.
        processed_url (str): The URL of the processed image.
    """
    __tablename__ = "processed_images"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String)
    processed_url = Column(String, unique=True)
