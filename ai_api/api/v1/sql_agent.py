from langchain_community.utilities import SQLDatabase
from langchain_community.llms import OpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from ai_api.models.models import User
# Загрузка переменных окружения из .env файла
load_dotenv()

# Подключение к базе данных PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
db = SQLDatabase(engine)
Session = sessionmaker(bind=engine)
session = Session()

OPEN_AI_TOKEN = os.getenv("OPEN_AI_TOKEN")
os.environ['OPENAI_API_KEY'] = OPEN_AI_TOKEN

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)



toolkit = SQLDatabaseToolkit(db=db, llm=llm)

async def analyze_expense_query(user_telegram_id: str, user_query: str, db_session: Session) -> dict:
    user = db_session.query(User).filter(User.telegram_id == user_telegram_id).first()

    if not user:
        return {"error": "User not found"}

    user_id = user.id


    custom_prefix = f"""
    Please make sure that all queries are filtered by user_id = {user_id}.
    If the currency is different, I need the data for each currency separately.
    If the question is about the total amount of money spent, without specifying a particular item or category of items, use the transactions table and the columns total_price and currency.
    If the question is about a specific item or category of items, use the purchases table and the columns category, item_name, quantity, price, and currency.
    All item categories in the purchases table are ["meat", "beverage", "dairy_product", "dessert", "fruit_and_vegi", "hygiene", "household_chem", "gift", "fish_product", "other"]
    Pay close attention to the date. If information is needed for a specific time period, handle it very carefully. This is critically important.
    """

    agent_executor = create_sql_agent(
        llm,
        toolkit=toolkit,
        prefix=custom_prefix,
        verbose=True
    )

    response = agent_executor.invoke({"input": user_query})
    return response['output']

# telegram_id = "123"  # переданный telegram_id
# user = session.query(User).filter(User.telegram_id == telegram_id).first()
#
# if user:
#     user_id = user.id
#     print(f"User ID: {user_id}")
# else:
#     user_id = 0
#     print("Пользователь не найден")
#
# custom_prefix = f"""You are an assistant for tracking personal expenses.
# Please make sure that all queries are filtered by user_id = {user_id}
# If the currency is different, I need the data for each currency separately.
# If the question is about the total amount of money spent, without specifying a particular item or category of items, use the transactions table and the columns total_price and currency.
# If the question is about a specific item or category of items, use the purchases table and the columns category, item_name, quantity, price, and currency.
# All item categories in the purchases table are ["meat", "beverage", "dairy_product", "dessert", "fruit_and_vegi", "hygiene", "household_chem", "gift", "fish_product", "other"]
# Product categories are always in English, but the items themselves may be in multiple languages and may be recorded differently. Keep this in mind.
# When you search for a specific item in the table, use the same language in which you are asked.
# Pay close attention to the date. If information is needed for a specific time period, handle it very carefully. This is critically important."""
#
#
# agent_executor = create_sql_agent(llm,
#                          toolkit=toolkit,
#                          prefix=custom_prefix,
#                          verbose=True)
#
#
#
#
# resp = agent_executor.invoke({"input": "когда я покупал пиво?"})
#
# print(resp['output'])
#
# # Пример использования агента
#
# # resp = agent_executor.invoke({"input": "сколько всего я потратил денег?"})
# #
# print(resp)