import os
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# Initialize the Wikipedia API wrapper with specified parameters
api_wrapper = WikipediaAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=256,
)

# Create a tool for querying Wikipedia
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


def save_to_text(data: str, filename: str = "research-output"):
    # Check if the output directory exists, create if not
    if "research-outputs" not in os.listdir():
        os.makedirs("research-outputs")

    # Generate a timestamp for the output file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format the text to be saved
    formatted_text = f"""––– Research Output –––\nTimestamp: {timestamp}\n\n{data}\n\n"""
    filename_with_timestamp = f"{filename} - {timestamp}.txt"
    filepath = os.path.join("research-outputs", filename_with_timestamp)

    # Write the formatted text to the output file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Research data successfully saved to {filename_with_timestamp}"


# Define a tool for saving research output to a text file
save_tool = Tool(
    name="save_to_text",
    description="""Save structured research output to a text file. 
    Parameters:
        data: The research output to save
        filename: Name for the output file (without extension)
    """,
    func=save_to_text,
)
