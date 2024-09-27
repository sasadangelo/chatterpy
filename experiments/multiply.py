from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from callbacks import AgentCallbackHandler
from langchain_core.tools import ToolException

PROMPT_TEMPLATE = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}].
    Action Input: the input to the action (in dictionary format).
    Observation: always analyze the result of the action.
    ... (this Thought/Action/Action Input/Observation could repeat N times until you don't find the final answer)
    Thought: I now know the final answer.
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """


prompt_template = PromptTemplate.from_template(template=PROMPT_TEMPLATE)

class MultiplyInput(BaseModel):
    a: int = Field(..., description="The first integer to multiply.")
    b: int = Field(..., description="The second integer to multiply.")

def multiply_func(a: int, b: int) -> int:
  """This function multiply two integers and return an integer."""
  return a*b

multiply = StructuredTool(name="multiply",
                          func=multiply_func,
                          description="This function multiply two integers and return an integer.",
                          args_schema=MultiplyInput,
                          return_direct=True,
                          handle_tool_error=True)

tools=[multiply]

model_name = "llama3.1"
base_url = "http://localhost:11434"

llm = ChatOllama(model=model_name, base_url=base_url, callbacks=[AgentCallbackHandler()])

#print(multiply.invoke({"a": 2, "b": 3}))
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=5)
agent_executor.invoke({"input": "Can you multiply 3 by 2 and give me the result?"})
