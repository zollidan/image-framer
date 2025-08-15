import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    BUCKET_NAME: str = os.getenv("BUCKET_NAME")
    ENDPOINT: str = os.getenv("ENDPOINT")
    ACCESS_KEY: str = os.getenv("ACCESS_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    ALLOWED_TYPES: list[str] = ["image/jpeg", "image/png", "application/pdf"]
    ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:80",
        "http://localhost",
        "http://app",
        "https://app"
    ]
    S3_PUBLIC_URL: str = "/s3/file"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()
