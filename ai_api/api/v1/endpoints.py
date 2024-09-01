from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Security
from ai_api.api.v1.whisper_service import transcribe_audio
from ai_api.core.utils import check_bearer_token, read_temp_data, delete_temp_data, save_to_db, write_temp_data
from datetime import datetime
from sqlalchemy.orm import Session
from ai_api.core.db import get_db
from ai_api.api.v1.text_analysis import analyze_text
import os

router = APIRouter()


@router.post("/query-expenses/")
async def query_expenses(user_id: int, query: str, api_key: str = Depends(check_bearer_token),
                         db: Session = Depends(get_db)):
    """
    Эндпоинт для анализа трат пользователя.

    :param user_id: Идентификатор пользователя (например, ID в Telegram).
    :param query: Текстовый запрос от пользователя (например, "Сколько я потратил на молоко в прошлом месяце?").
    :param api_key: Bearer-токен для авторизации.
    :param db: Сессия базы данных.
    :return: Результат анализа трат.
    """
    # Здесь будет логика анализа запроса и выполнения соответствующего SQL-запроса

    # Для примера: просто возвращаем то, что получил эндпоинт
    return {"user_id": user_id, "query": query, "result": "Здесь будет результат анализа запроса"}

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



@router.post("/submit-text/")
async def submit_text(user_id: int, text: str, api_key: str = Depends(check_bearer_token), db: Session = Depends(get_db)):
    # Анализируем текст
    analyzed_data = analyze_text(text)

    # Сохраняем результат анализа в постоянное хранилище
    timestamp = datetime.now().isoformat()
    save_to_db(db, user_id, analyzed_data, timestamp)

    # Возвращаем результат анализа пользователю для проверки
    return {"status": "success", "analyzed_data": analyzed_data}




# @router.post("/submit-text/")
# async def submit_text(user_id: int, text: str, api_key: str = Depends(check_bearer_token)):
#     # Анализируем текст
#     analyzed_data = analyze_text(text)
#
#     # Сохраняем результат анализа в постоянное хранилище
#     timestamp = datetime.now().isoformat()
#     save_to_db(user_id, analyzed_data, timestamp)
#
#     # Возвращаем результат анализа пользователю для проверки
#     return {"status": "success", "analyzed_data": analyzed_data}
# @router.post("/confirm-text/")
# async def confirm_text(user_id: int, confirmation: bool, token: str = Security(check_bearer_token)):
#     temp_data = read_temp_data(user_id)
#
#     if not temp_data:
#         raise HTTPException(status_code=404, detail="No temporary data found for the user.")
#
#     if confirmation:
#         analyzed_data = analyze_text(temp_data["text"])
#         save_to_db(user_id, analyzed_data)  # Сохраняем данные в постоянное хранилище
#         delete_temp_data(user_id)  # Удаляем временные данные
#         return {"status": "success", "analyzed_data": analyzed_data}
#     else:
#         delete_temp_data(user_id)  # Удаляем временные данные
#         return {"status": "failure", "message": "Session ended, data not confirmed."}
