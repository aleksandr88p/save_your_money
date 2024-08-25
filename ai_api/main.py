from fastapi import FastAPI
from ai_api.api.v1.endpoints import router as api_router

app = FastAPI(
    title="AI API",
    description="API for testing and integrating AI models",
    version="1.0.0"
)

# Подключение маршрутов из endpoints.py
app.include_router(api_router, prefix="/api/v1")

# Заглушка для главной страницы
@app.get("/")
async def read_root():
    return {"message": "Welcome to AI API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
