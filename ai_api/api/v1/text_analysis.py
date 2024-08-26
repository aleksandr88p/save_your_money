from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms import HuggingFacePipeline






# # Попробуем Phi-3-mini-instruct
# model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)
# tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
#
# pipe = pipeline('text-generation', device=0, model=model, tokenizer=tokenizer,
#                max_new_tokens=200,
#                )
#
# llm = HuggingFacePipeline(pipeline=pipe)
#
#
def analyze_text(text: str) -> dict:
    # Здесь будет логика для анализа текста и разбиения по категориям
    return {"categories": "example_category", "items": "example_item"}
# import torch
# torch.cuda.empty_cache()

