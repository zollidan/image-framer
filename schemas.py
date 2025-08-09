# schemas.py
from pydantic import BaseModel

# Схема для ответа пользователю после успешной обработки
class ImageResponse(BaseModel):
    filename: str
    url: str

    class Config:
        orm_mode = True # Позволяет Pydantic работать с моделями SQLAlchemy