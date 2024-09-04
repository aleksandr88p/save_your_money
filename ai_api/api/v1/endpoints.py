from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Security
from ai_api.api.v1.whisper_service import transcribe_audio
from ai_api.core.utils import check_bearer_token, read_temp_data, delete_temp_data, save_to_db, write_temp_data
from datetime import datetime
from sqlalchemy.orm import Session
from ai_api.core.db import get_db
from ai_api.api.v1.text_analysis import analyze_text
from ai_api.api.v1.sql_agent import analyze_expense_query

import os

router = APIRouter()


@router.post("/query-expenses/")
async def query_expenses(user_telegram_id: str, query: str, api_key: str = Depends(check_bearer_token), db: Session = Depends(get_db)):
    print(user_telegram_id)
    response = await analyze_expense_query(user_telegram_id, query, db)

    if "error" in response:
        raise HTTPException(status_code=404, detail=response["error"])

    return {"status": "success", "response": response}



@router.post("/confirm-text/")
async def confirm_text(user_id: int, confirmation: bool, api_key: str = Depends(check_bearer_token),
                       db: Session = Depends(get_db)):
    if confirmation:
        # Извлекаем текст из временного хранилища
        temp_data = read_temp_data(user_id)
        if not temp_data:
            raise HTTPException(status_code=404, detail="No temporary data found for this user.")

        analyzed_data = analyze_text(temp_data["text"])

        # Сохраняем данные в базе данных
        save_to_db(db, user_id, analyzed_data, temp_data["timestamp"])

        # Удаляем временные данные
        delete_temp_data(user_id)

        return {"status": "success", "analyzed_data": analyzed_data}
    else:
        # Удаляем временные данные при отказе
        delete_temp_data(user_id)
        return {"status": "failure", "message": "Please correct the text manually."}
    
@router.post("/audio-to-text/")
async def audio_to_text(user_id: int, file: UploadFile = File(...), token: str = Security(check_bearer_token)):
    try:
        # Проверка существования директории и её создание
        if not os.path.exists('temp_audio'):
            os.makedirs('temp_audio')
        
        # Логирование размера загружаемого файла
        file_size = await file.read()
        print(f"File size: {len(file_size)} bytes")
        await file.seek(0)  # Возвращаем указатель чтения в начало файла
        
        # Сохранение файла временно
        file_location = f"temp_audio/{file.filename}"
        print(f"Saving file to: {file_location}")
        
        with open(file_location, "wb") as buffer:
            buffer.write(file_size)

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
        raise HTTPException(status_code=500, detail=f"Error while processing audio: {str(e)}")
    finally:
        try:
            # Удаление временного файла после обработки
            os.remove(file_location)
            print(f"File {file_location} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete file: {e}")


@router.get("/get-temp-text/")
async def get_temp_text(user_id: int, token: str = Security(check_bearer_token)):
    temp_data = read_temp_data(user_id)

    if not temp_data:
        raise HTTPException(status_code=404, detail="No temporary data found for this user.")

    return {"user_id": user_id, "text": temp_data["text"], "timestamp": temp_data["timestamp"]}



@router.post("/submit-text/")
async def submit_text(user_id: int, text: str, api_key: str = Depends(check_bearer_token), db: Session = Depends(get_db)):
    # Анализируем текст
    analyzed_data = analyze_text(text)

    # Сохраняем результат анализа в постоянное хранилище
    timestamp = datetime.now().isoformat()
    save_to_db(db, user_id, analyzed_data, timestamp)

    # Возвращаем результат анализа пользователю для проверки
    return {"status": "success", "analyzed_data": analyzed_data}




