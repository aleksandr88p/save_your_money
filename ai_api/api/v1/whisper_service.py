import whisper
import os
from fastapi import HTTPException

# Загружаем модель Whisper
model = whisper.load_model("small", device="cpu")

def transcribe_audio(file_path: str) -> str:
    try:
        result = model.transcribe(file_path)
        recognized_text = result["text"]
        return recognized_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке аудио: {str(e)}")
    finally:
        # Удаляем временный файл после обработки
        os.remove(file_path)
