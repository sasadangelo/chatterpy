from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from callbacks import AgentCallbackHandler
from langchain_core.tools import ToolException
import json
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.tools import tool

load_dotenv(".env")

PROMPT_TEMPLATE = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format strictly:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, **must be exactly** one of [{tool_names}]. No other variations (such as capital letters, backticks, or extra words) are allowed.
    Action Input: the input to the action. It MUST BE in valid and complete JSON format (es. {{"a": 3, "b": 2}}).
    Observation: always analyze the result of the action.
    ... (this Thought/Action/Action Input/Observation could repeat N times until you don't find the final answer)
    Thought: I now know the final answer.
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

class MultiplyInput(BaseModel):
    a: int = Field(..., description="The first integer to multiply.")
    b: int = Field(..., description="The second integer to multiply.")

# pydantic_parser = PydanticOutputParser(pydantic_object=MultiplyInput)


prompt_template = PromptTemplate.from_template(template=PROMPT_TEMPLATE)

# @tool
# def multiply(input: str) -> str:
#   """This function multiplies two integers and returns an integer."""
#   print(f"Multiplying {input}")
#   return "6"

def multiply_func(a: int, b: int) -> int:
  """This function multiplies two integers and returns an integer."""
  print(f"Multiplying {a} by {b}")
  return a*b

multiply = StructuredTool(name="multiply",
                          func=multiply_func,
                          description="This function multiplies two integers and returns an integer.",
                          args_schema=MultiplyInput,
                          return_direct=True,
                          handle_tool_error=True)

tools=[multiply]

model_name = "llama3.1"
base_url = "http://localhost:11434"

llm = ChatOllama(model=model_name,
                 base_url=base_url,
                 callbacks=[AgentCallbackHandler()],
                 temperature=0,
                 stop=["\nObservation:"])

# def parse_action_input(action_input):
#     try:
#         return json.loads(action_input)
#     except json.JSONDecodeError as e:
#         raise ToolException(f"Invalid JSON format: {e}")

# # Override the run method to parse the action input
# multiply.run = lambda action_input: multiply_func(**parse_action_input(action_input))


#print(multiply.invoke({"a": 2, "b": 3}))
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
result = agent_executor.invoke({"input": "Can you multiply 3 by 2 and give me the result?"})
print(result['output'])
