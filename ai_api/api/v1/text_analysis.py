from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

load_dotenv()

OPEN_AI_TOKEN = os.getenv("OPEN_AI_TOKEN")
os.environ['OPENAI_API_KEY'] = OPEN_AI_TOKEN

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)



meat_schema = ResponseSchema(
    name="meat",
    description="List of meat products(all type of meat products) with name, quantity, and price",
    type="Dict",
)

beverage_schema = ResponseSchema(
    name="beverage",
    description="List of beverages with name, quantity, and price",
    type="Dict",
)

dairy_product_schema = ResponseSchema(
    name="dairy_product",
    description="List of dairy products with name, quantity, and price",
    type="Dict",
)
dessert_schema = ResponseSchema(
    name="dessert",
    description="List of desserts with name, quantity, and price",
    type="Dict",
)
fruit_and_vegi_schema = ResponseSchema(
    name="fruit_and_vegi",
    description="List of fruits and vegetables with name, quantity, and price",
    type="Dict",
)
hygiene_schema = ResponseSchema(
    name="hygiene",
    description="List of hygiene products with name, quantity, and price",
    type="Dict",
)
household_chem_schema = ResponseSchema(
    name="household_chem",
    description="List of household chemy products with name, quantity, and price",
    type="Dict",
)
gift_schema = ResponseSchema(
    name="gift",
    description="List of all gifts and souvenirs products with name, quantity, and price",
    type="Dict",
)

fish_product_schema = ResponseSchema(
    name="fish_product",
    description="List of fish products with name, quantity, and price",
    type="Dict",
)
other_schema = ResponseSchema(
    name="other",
    description="List of meat products with name, quantity, and price",
    type="Dict",
)

total_price_schema = ResponseSchema(
    name="total_price",
    description="Total price of all products",
    type="string"
)

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

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()

prompt_template = """
Extract information from the text according to the instructions.
Always include the currency if it is mentioned in the text. If the quantity is not specified, write "None."

text: {text}

format_instructions: {format_instructions}
"""

example_text = "I bought 2 kg of chicken breasts for 500 rubles, 1 kg of beef for 300 rubles."
example_text2 = "Я купил фарш одну пачку на 300 рублей, кока колу на 500 рублей, а и еще я купил сосиски говяжьи 400 грамм на 250 рублей и торт прага - он стоил около 700 рублей, так же я купил розы жене на 1000 рублей, и еще я купил кефир 1 литр он стоил 100 рублей"


def analyze_text(text: str) -> dict:
    prompt = ChatPromptTemplate.from_template(prompt_template)
    messages = prompt.format_messages(text=text, format_instructions=format_instructions)

    response = llm.invoke(input=messages)
    print(response.content)
    output_dict = output_parser.parse(response.content)
    return output_dict

