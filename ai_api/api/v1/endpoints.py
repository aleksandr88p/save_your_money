from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Security
from ai_api.api.v1.whisper_service import transcribe_audio
from ai_api.core.utils import check_bearer_token, read_temp_data, delete_temp_data, save_to_db, write_temp_data

from ai_api.api.v1.text_analysis import analyze_text
import os

router = APIRouter()


@router.post("/confirm-text/")
async def confirm_text(user_id: int, confirmation: bool, token: str = Security(check_bearer_token)):
    temp_data = read_temp_data(user_id)

    if not temp_data:
        raise HTTPException(status_code=404, detail="No temporary data found for the user.")

    if confirmation:
        analyzed_data = analyze_text(temp_data["text"])
        save_to_db(user_id, analyzed_data)  # Сохраняем данные в постоянное хранилище
        delete_temp_data(user_id)  # Удаляем временные данные
        return {"status": "success", "analyzed_data": analyzed_data}
    else:
        delete_temp_data(user_id)  # Удаляем временные данные
        return {"status": "failure", "message": "Session ended, data not confirmed."}

@router.post("/audio-to-text/")
async def audio_to_text(user_id: int, file: UploadFile = File(...), token: str = Security(check_bearer_token)):
    try:
        # Сохранение файла временно
        file_location = f"temp_audio/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # Преобразование аудио в текст
        recognized_text = transcribe_audio(file_location)

        # Сохранение текста во временное хранилище
        write_temp_data(user_id, recognized_text)

        return {
            "filename": file.filename,
            "recognized_text": recognized_text,
            "confirmation_required": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while processing audio")
    finally:
        try:
            os.remove(file_location)  # Удаление временного файла после обработки
        except Exception as e:
            print('file deleted\n{}'.format(e))


@router.get("/get-temp-text/")
async def get_temp_text(user_id: int, token: str = Security(check_bearer_token)):
    temp_data = read_temp_data(user_id)

    if not temp_data:
        raise HTTPException(status_code=404, detail="No temporary data found for this user.")

    return {"user_id": user_id, "text": temp_data["text"], "timestamp": temp_data["timestamp"]}

