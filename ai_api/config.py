# config.py

import os
from dotenv import load_dotenv
load_dotenv()  # Загружаем переменные окружения из .env файла


class Config:
    APP_NAME = "AI API"
    APP_DESCRIPTION = "API for testing and integrating AI models"
    APP_VERSION = "1.0.0"

    # Параметры запуска приложения
    HOST = os.getenv("APP_HOST", "0.0.0.0")
    PORT = int(os.getenv("APP_PORT", 8000))
    RELOAD = os.getenv("APP_RELOAD", "True").lower() in ("true", "1", "yes")

    # Параметры подключения к базе данных
    POSTGRES_USER = os.getenv("POSTGRES_USER", "your_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "your_password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "your_db_name")
    POSTGRES_URL = os.getenv("POSTGRES_URL", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    # Параметры API токена
    API_HEADER_TOKEN = os.getenv('API_HEADER_TOKEN', 'your_default_token')

    # Параметры временного хранилища данных
    TEMP_DATA_FILE = os.getenv("TEMP_DATA_FILE", "temp_data.json")

    # Параметры OpenAI
    OPEN_AI_TOKEN = os.getenv("OPEN_AI_TOKEN", "your_openai_token")

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_URL}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


config = Config()
