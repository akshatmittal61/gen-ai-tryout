import os
from config import groq_key
# from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# os.environ['OPENAI_API_KEY'] = openapi_key
#
# llm = HuggingFacePipeline.from_model_id(
#     model_id="gpt2",
#     task="text-generation",
#     pipeline_kwargs={"max_new_tokens": 10},
#     device=-1
# )

os.environ['GROQ_API_KEY'] = groq_key

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

# questions = [
#     "What is current population of the world",
#     "What are symlinks"
# ]

question = "What are symlinks"
chain = prompt | llm
print(chain.invoke({"question": question}))

# for question in questions:
#     print(chain.invoke({"question": question}))
