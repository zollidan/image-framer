import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BUCKET_NAME: str
    ENDPOINT: str
    ACCESS_KEY: str
    SECRET_KEY: str
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    ALLOWED_TYPES: list[str] = ["image/jpeg", "image/png", "application/pdf"]
    ORIGINS: list[str] = [
        "http://localhost:5173",
    ]
    S3_PUBLIC_URL: str = "/s3/file"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()
