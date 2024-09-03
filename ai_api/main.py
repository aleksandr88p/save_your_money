# main.py

from fastapi import FastAPI
from ai_api.api.v1.endpoints import router as api_router
from ai_api.config import config  # Подключаем конфигурацию

# Создание экземпляра приложения FastAPI с параметрами из конфигурации
app = FastAPI(
    title=config.APP_NAME,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION
)

# Подключение маршрутов из endpoints.py с префиксом /api/v1
app.include_router(api_router, prefix="/api/v1")

# Простой эндпоинт для проверки работы приложения
@app.get("/")
async def read_root():
    """
    Возвращает приветственное сообщение при обращении к корневому маршруту.
    """
    return {"message": "Welcome to AI API"}

# Точка входа для запуска приложения с помощью uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT, reload=config.RELOAD)
