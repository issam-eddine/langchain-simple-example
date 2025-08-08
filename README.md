# langchain-simple-example

This repository showcases the use of LangChain to create an agent that can respond to queries. It can use tools for searching Wikipedia and saving the results to a file.

A simple example of how to use langchain to invoke an LLM:

``` python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4.1-mini")
response = llm.invoke("What is the capital of the moon?")
print(response.content)
```
