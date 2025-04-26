import os
from config import groq_key
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

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

question = "What are symlinks"
chain = prompt | llm
print(chain.invoke({"question": question}))
