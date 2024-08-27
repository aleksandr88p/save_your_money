from fastapi import APIRouter, UploadFile, File, HTTPException
from ai_api.api.v1.whisper_service import transcribe_audio
from ai_api.api.v1.text_analysis import analyze_text
from ai_api.core.utils import write_data
import os

router = APIRouter()

@router.post("/audio-to-text/")
async def audio_to_text(file: UploadFile = File(...)):
    try:
        file_location = f"temp_audio/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        recognized_text = transcribe_audio(file_location)

        return {
            "filename": file.filename,
            "recognized_text": recognized_text,
            "confirmation_required": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке аудио: {str(e)}")

@router.post("/confirm-text/")
async def confirm_text(user_id: int, confirmation: bool, text: str):
    if confirmation:
        analyzed_data = analyze_text(text)
        write_data(user_id, analyzed_data)  # Сохраняем данные в JSON-файл
        return {"status": "success", "analyzed_data": analyzed_data}
    else:
        return {"status": "failure", "message": "Please correct the text manually."}
