from sqlalchemy import create_engine
from dotenv import load_dotenv
from models import User, Purchase, Transaction  # Импортируем модели
import os
# Загрузка переменных окружения из .env файла
load_dotenv()

# Создаем базу данных SQLAlchemy
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

# Создаем таблицы в базе данных
def init_db():
    User.__table__.create(bind=engine, checkfirst=True)
    Purchase.__table__.create(bind=engine, checkfirst=True)
    Transaction.__table__.create(bind=engine, checkfirst=True)

if __name__ == "__main__":
    init_db()
    print("База данных и таблицы успешно созданы.")
