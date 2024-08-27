import json
from datetime import datetime
TEMP_DATA_FILE = "temp_data.json"

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
