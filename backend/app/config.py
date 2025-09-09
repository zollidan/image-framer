import os
from pydantic_settings import BaseSettings, SettingsConfigDict


import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class loads configuration variables from a .env file and the environment.
    It uses pydantic-settings to manage application settings.

    Attributes:
        BUCKET_NAME (str): The name of the S3 bucket.
        ENDPOINT (str): The S3 endpoint URL.
        ACCESS_KEY (str): The access key for the S3 bucket.
        SECRET_KEY (str): The secret key for the S3 bucket.
        MAX_FILE_SIZE (int): The maximum allowed file size for uploads in bytes.
        ALLOWED_TYPES (list[str]): A list of allowed MIME types for file uploads.
        ORIGINS (list[str]): A list of allowed origins for CORS.
        S3_PUBLIC_URL (str): The public URL prefix for accessing S3 files.
    """
    BUCKET_NAME: str = ""
    ENDPOINT: str = ""
    ACCESS_KEY: str = ""
    SECRET_KEY: str = ""
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    ALLOWED_TYPES: list[str] = ["image/jpeg", "image/png", "application/pdf"]
    ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:80",
        "http://localhost",
        "https://zollidan-image-framer-4c80.twc1.net",
    ]
    S3_PUBLIC_URL: str = "/s3/file"

    # model_config = SettingsConfigDict(
    #     env_file=os.path.join(os.path.dirname(
    #         os.path.abspath(__file__)), "..", ".env")
    # )


settings = Settings()
