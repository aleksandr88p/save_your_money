from traceback import print_tb

from langchain_community.utilities import SQLDatabase
from langchain_community.llms import OpenAI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ai_api.config import config  # Подключаем конфигурацию

import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from ai_api.models.models import User

# Подключение к базе данных PostgreSQL через конфигурацию
engine = create_engine(config.DATABASE_URL)
db = SQLDatabase(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Настройка OpenAI через конфигурацию
os.environ['OPENAI_API_KEY'] = config.OPEN_AI_TOKEN

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)


async def analyze_expense_query(user_telegram_id: str, user_query: str, db_session: Session) -> dict:
    print(user_telegram_id, user_query)
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
