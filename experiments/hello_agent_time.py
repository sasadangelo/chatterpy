from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
import datetime
from langchain.agents import tool

def get_react_prompt_template():
    return PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

@tool
def get_system_time(ignore: str) -> str:
    """
    Returns the current date and time in the default format.

    This function does not take any parameters. It returns the current date and time
    formatted according to the default format '%Y-%m-%d %H:%M:%S'.

    Returns:
    - str: The current date and time as a string in the format '%Y-%m-%d %H:%M:%S'.

    Example:
    >>> get_system_time()
    '2024-09-09 14:25:30'
    """
    # get the current date and time
    current_time = datetime.datetime.now()
    # format the time as a string in the format "YYYY-MM-DD HH:MM:SS"
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # return the formatted time
    return formatted_time

load_dotenv()

model_name = "llama3.1"
base_url = "http://localhost:11434"

llm = ChatOllama(model=model_name, base_url=base_url)

query = "What is the date and time now?"
#prompt_template = hub.pull("hwchase17/react")
prompt_template = get_react_prompt_template()
tools=[get_system_time]
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
result = agent_executor.invoke({"input": query})
print(result)