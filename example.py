import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4.1-mini")
# llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="openai/gpt-oss-20b")

response = llm.invoke("What is the capital of the moon?")
print(response.content)
