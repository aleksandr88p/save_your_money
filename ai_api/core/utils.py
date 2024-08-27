import json
import os
from datetime import datetime


def read_data(file_path='data.json'):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_data(user_id, data_to_save, file_path='data.json'):
    data = read_data(file_path)

    if str(user_id) not in data:
        data[str(user_id)] = []

    data[str(user_id)].append({
        "timestamp": datetime.now().isoformat(),
        "data": data_to_save
    })

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
