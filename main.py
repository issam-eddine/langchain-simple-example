import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import wikipedia_tool, save_tool

load_dotenv()


# Define the structure of the research response
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# Initialize the language model
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4.1-mini")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Initialize the output parser
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help with research queries.
            Provide a final response in this exact JSON format:
            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# List of tools available to the agent
tools = [wikipedia_tool, save_tool]

# Create the agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Enable verbose output for debugging
)

# Get user input for research query
user_query = input("what can I help you research?" + "\n" * 2)

# Execute the agent with the user's query
raw_response = agent_executor.invoke({"query": user_query})

# Print the raw output from the agent
print(f"raw output: {raw_response['output']}")

try:
    # Parse the raw output into a structured format
    structured_response = parser.parse(raw_response["output"])

    # Print the structured response
    print()
    print(f"structured response:")
    print(f"topic: {structured_response.topic}")
    print(f"summary: {structured_response.summary}")
    print(f"sources: {', '.join(structured_response.sources)}")
    print(f"tools_used: {', '.join(structured_response.tools_used)}")

except Exception as e:
    # Handle parsing errors
    print()
    print(f"note: could not parse structured response: {e}")
