import os
from pydantic_settings import BaseSettings  # вместо pydantic

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    OPENAI_API_KEY: str
    MODEL: str
    BASE_URL: str
    API_URL: str
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        env_file_encoding = "utf-8"

settings = Settings()
