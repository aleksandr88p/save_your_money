import json
from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

load_dotenv()
api_header_token = os.getenv('api_header_token')
API_KEY = api_header_token
api_key_header = APIKeyHeader(name="Authorization")

TEMP_DATA_FILE = "temp_data.json"


def check_bearer_token(api_key_header: str = Security(api_key_header)):
    if api_key_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key_header


def write_temp_data(user_id: int, text: str):
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
    try:
        with open(TEMP_DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    return data.get(str(user_id), None)
