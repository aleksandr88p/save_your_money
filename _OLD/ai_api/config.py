# config.py

import os

class Config:
    APP_NAME = "AI API"
    APP_DESCRIPTION = "API for testing and integrating AI models"
    APP_VERSION = "1.0.0"

    # Параметры запуска приложения
    HOST = os.getenv("APP_HOST", "0.0.0.0")
    PORT = int(os.getenv("APP_PORT", 8000))
    RELOAD = os.getenv("APP_RELOAD", "True").lower() in ("true", "1", "yes")

config = Config()
