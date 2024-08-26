from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

load_dotenv()

OPEN_AI_TOKEN = os.getenv("OPEN_AI_TOKEN")
os.environ['OPENAI_API_KEY'] = OPEN_AI_TOKEN
# llm = ChatOpenAI(temperature=0.0)

# meat_schema = ResponseSchema(name="meat",
#                              description="")
# beverage_schema = ResponseSchema(name="beverage",
#                                  description="")
# dairy_product_schema = ResponseSchema(name="dairy_product",
#                                       description="")
# dessert_schema = ResponseSchema(name="dessert",
#                                 description="")
# fruit_and_vegi_schema = ResponseSchema(name="fruit_and_vegi",
#                                        description="")
# hygiene_schema = ResponseSchema(name="hygiene",
#                                 description="")
# household_chem_schema = ResponseSchema(name="household_chem",
#                                        description="")
# gift_schema = ResponseSchema(name="gift",
#                              description="")
#
# fish_product_schema = ResponseSchema(name="fish_product", description="")
# other_schema = ResponseSchema(name="other",
#                               description="")
#
# total_price_schema = ResponseSchema(name="total_price", description="")


# Схема для одного товара
item_schema = ResponseSchema(name="item",
                             description="Contains information about the product",
                             fields={
                                 "name": {"type": "string", "description": "The name of the product"},
                                 "quantity": {"type": "string", "description": "The quantity of the product"},
                                 "price": {"type": "string", "description": "The price of the product"}
                             })

# Схемы для категорий товаров, содержащие списки товаров
meat_schema = ResponseSchema(name="meat",
                             description="List of meat products",
                             fields={"items": {"type": "list", "items": item_schema}})

beverage_schema = ResponseSchema(name="beverage",
                                 description="List of beverages",
                                 fields={"items": {"type": "list", "items": item_schema}})

dairy_product_schema = ResponseSchema(name="dairy_product",
                                      description="List of dairy products",
                                      fields={"items": {"type": "list", "items": item_schema}})

dessert_schema = ResponseSchema(name="dessert",
                                description="List of desserts",
                                fields={"items": {"type": "list", "items": item_schema}})

fruit_and_vegi_schema = ResponseSchema(name="fruit_and_vegi",
                                       description="List of fruits and vegetables",
                                       fields={"items": {"type": "list", "items": item_schema}})

hygiene_schema = ResponseSchema(name="hygiene",
                                description="List of hygiene products",
                                fields={"items": {"type": "list", "items": item_schema}})

household_chem_schema = ResponseSchema(name="household_chem",
                                       description="List of household chemicals",
                                       fields={"items": {"type": "list", "items": item_schema}})

gift_schema = ResponseSchema(name="gift",
                             description="List of gifts",
                             fields={"items": {"type": "list", "items": item_schema}})

fish_product_schema = ResponseSchema(name="fish_product",
                                     description="List of fish products",
                                     fields={"items": {"type": "list", "items": item_schema}})

other_schema = ResponseSchema(name="other",
                              description="List of other products",
                              fields={"items": {"type": "list", "items": item_schema}})

# Схема для общей цены
total_price_schema = ResponseSchema(name="total_price",
                                    description="Total price of all products",
                                    fields={"value": {"type": "string", "description": "The total price"}})

response_schemas = [
    meat_schema,
    beverage_schema,
    dairy_product_schema,
    dessert_schema,
    fruit_and_vegi_schema,
    hygiene_schema,
    household_chem_schema,
    gift_schema,
    fish_product_schema,
    other_schema,
    total_price_schema
]
# Создаем StructuredOutputParser с заданными схемами
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

prompt_template = """
Extract information from the text according to the instructions.

text: {text}

format_instructions: {format_instructions}
"""

# Создаем ChatPromptTemplate с использованием метода from_template
prompt = ChatPromptTemplate.from_template(prompt_template)

# Пример использования: Ввод текста для анализа
example_text = "I bought 2 kg of chicken breasts for 500 rubles, 1 kg of beef for 300 rubles."

# Форматируем сообщения для использования в модели
messages = prompt.format_messages(text=example_text,
                                  format_instructions=format_instructions)



# Инициализируем модель OpenAI Chat
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
# Отправляем запрос и получаем ответ

response = llm.invoke(input=messages)
print(response.content)
# parsed_response = output_parser.invoke(response[0].content)
#
# # Печать ответа модели
# print(parsed_response)





def analyze_text(text: str) -> dict:
    # Здесь будет логика для анализа текста и разбиения по категориям
    return {"categories": "example_category", "items": "example_item"}
# import torch
# torch.cuda.empty_cache()
