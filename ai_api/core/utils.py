import json
from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from ai_api.models.models import Purchase, Transaction, User
from sqlalchemy.orm import Session

load_dotenv()
api_header_token = os.getenv('api_header_token')
API_KEY = api_header_token
api_key_header = APIKeyHeader(name="Authorization")

TEMP_DATA_FILE = "temp_data.json"
DB_DATA_FILE = "db_data.json"

def check_bearer_token(api_key_header: str = Security(api_key_header)):
    if api_key_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key_header


def save_to_db(db: Session, user_id: int, analyzed_data: dict, timestamp=None):
    # Проверка, существует ли пользователь
    user = db.query(User).filter(User.telegram_id == str(user_id)).first()
    if not user:
        # Если пользователя нет, создаем его
        user = User(telegram_id=str(user_id))
        db.add(user)
        db.commit()
        db.refresh(user)

    # Сохраняем покупки в таблицу purchases
    total_price = 0.0
    currency = ""
    for category, items in analyzed_data.items():
        if category == "total_price":
            total_price = float(items.split()[0])
            currency = items.split()[1]
        elif isinstance(items, list):
            for item in items:
                # Если данных нет, используем значение по умолчанию
                item_name = item.get('name', 'Unknown')
                quantity = item.get('quantity', None)
                price_str = item.get('price', None)
                price_value = None
                item_currency = None

                if price_str and price_str != "None":
                    price_parts = price_str.split()
                    if len(price_parts) == 2:
                        price_value = float(price_parts[0])
                        item_currency = price_parts[1]
                    else:
                        price_value = float(price_parts[0])

                purchase = Purchase(
                    user_id=user.id,
                    category=category,
                    item_name=item_name,
                    quantity=quantity,
                    price=price_value,
                    currency=item_currency,
                    timestamp=datetime.fromisoformat(timestamp)
                )
                db.add(purchase)
        else:
            # Если items не является списком, обрабатываем его как единичный элемент
            item_name = items.get('name', 'Unknown')
            quantity = items.get('quantity', None)
            price_str = items.get('price', None)
            price_value = None
            item_currency = None

            if price_str and price_str != "None":
                price_parts = price_str.split()
                if len(price_parts) == 2:
                    price_value = float(price_parts[0])
                    item_currency = price_parts[1]
                else:
                    price_value = float(price_parts[0])

            purchase = Purchase(
                user_id=user.id,
                category=category,
                item_name=item_name,
                quantity=quantity,
                price=price_value,
                currency=item_currency,
                timestamp=datetime.fromisoformat(timestamp)
            )
            db.add(purchase)

    # Сохраняем транзакцию
    if total_price > 0.0:
        transaction = Transaction(
            user_id=user.id,
            total_price=total_price,
            currency=currency,
            timestamp=datetime.fromisoformat(timestamp)
        )
        db.add(transaction)

    db.commit()


def write_temp_data(user_id: int, text: str):
    '''
    write temporal data after audio recognizion
    :param user_id:
    :param text:
    :return:
    '''
    try:
        with open(TEMP_DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    timestamp = datetime.now().isoformat()

    data[user_id] = {
        "text": text,
        "timestamp": timestamp
    }

    with open(TEMP_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def read_temp_data(user_id: int):
    """
    read temporal data after audio recognizion
    :param user_id:
    :return:
    """
    try:
        with open(TEMP_DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    return data.get(str(user_id), None)


def delete_temp_data(user_id: int):
    """
    delete temporal data after audio recognizion
    :param user_id:
    :return:
    """
    try:
        with open(TEMP_DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    if str(user_id) in data:
        del data[str(user_id)]

    with open(TEMP_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)






# def save_to_db(user_id: int, analyzed_data: dict, timestamp=None):
#     try:
#         with open(DB_DATA_FILE, "r", encoding='utf-8') as file:
#             all_data = json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError):
#         all_data = {}
#
#     if not timestamp:
#         # Извлекаем таймстамп из временного хранилища
#         temp_data = read_temp_data(user_id)
#         timestamp = temp_data['timestamp']
#
#     if str(user_id) in all_data:
#         all_data[str(user_id)].append({"data": analyzed_data, "timestamp": timestamp})
#     else:
#         all_data[str(user_id)] = [{"data": analyzed_data, "timestamp": timestamp}]
#
#     with open("db_data.json", "w", encoding='utf-8') as file:
#         json.dump(all_data, file, indent=4, ensure_ascii=False)

