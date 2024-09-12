from dotenv import load_dotenv
from langchain_core.tools import tool
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


tools = [add, multiply]

model_name = "llama3.1"
base_url = "http://localhost:11434"

llm = ChatOllama(model=model_name, base_url=base_url)

# model_name = "llama-2-7b-chat"
# base_url = "http://localhost:8000/v1"

# llm = ChatOpenAI(model=model_name, openai_api_base=base_url)

llm_forced_to_multiply = llm.bind_tools(tools, tool_choice="multiply")
ai_message = llm_forced_to_multiply.invoke("what is 2 + 4")
print(ai_message)