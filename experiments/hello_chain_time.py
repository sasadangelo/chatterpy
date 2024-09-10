import sys
from dotenv import load_dotenv
import datetime
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain.agents import tool

def get_react_prompt_template():
    return PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: The date and time format (i.e. '%Y-%m-%d %H:%M:%S')
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Returns the current date and time in the '%Y-%m-%d %H:%M:%S' format.
    """
    # get the current date and time
    current_time = datetime.datetime.now()
    # format the time as a string in the format "YYYY-MM-DD HH:MM:SS"
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print("CURRENT TIME is: ", formatted_time)
    # return the formatted time
    return formatted_time

# load environment variables
load_dotenv()

model_name = "llama3.1"
base_url = "http://localhost:11434"

llm = ChatOllama(model=model_name, base_url=base_url)

tools=[get_system_time]

# get the tools list
#tools_list=render_text_description(list(tools))
tool_names=", ".join([t.name for t in tools])

# set my message
query = "What is the current time?"
prompt_template = get_react_prompt_template()

# print out the prompt
print(prompt_template.format(input=query, tools=tools, tool_names=tool_names, agent_scratchpad=""))

# execute
output_parser = StrOutputParser()
llm.bind_tools(tools)
chain = prompt_template | llm | output_parser
#result = chain.invoke({"input": query})
result = chain.invoke({"input": query, "tools": tools, "tool_names": tool_names, "agent_scratchpad": ""})

# print out the result
print(result)