from typing import Union, List, Sequence, Optional, Tuple
from langchain.agents import tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool
#from langchain.tools.render import ToolsRenderer, render_text_description
from langchain_core.tools.render import ToolsRenderer, render_text_description
from callbacks import AgentCallbackHandler
from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain.agents import AgentOutputParser
from langchain.agents import create_react_agent, AgentExecutor

#from __future__ import annotations
#from typing import List, Optional, Sequence, Union
#from langchain_core.tools.render import ToolsRenderer, render_text_description
#from langchain.agents.format_scratchpad import format_log_to_str
#from langchain.agents.output_parsers import ReActSingleInputOutputParser


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    #print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # stripping away non alphabetic characters just in case

    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")

if __name__ == "__main__":
    print("Hello ReAct LangChain!")
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}] (ONLY the raw tool name, don't add unnecessary text)
    Action Input: the input to the action (ONLY the raw input, do not add any descriptors like 'text=')
    Observation: always analyze the result of the action, it should be the size in characters of the input word.
    ... (this Thought/Action/Action Input/Observation can repeat N times if you don't find the final answer)
    Thought: I now know the final answer, it should be the number of characters of the input word.
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """
    model_name = "llama3.1"
    base_url = "http://localhost:11434"

    prompt_template = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )


    llm = ChatOllama(
        model=model_name,
        base_url=base_url,
        temperature=0,
        stop=["\nObservation", "Observation"],
        callbacks=[AgentCallbackHandler()],
    )


    intermediate_steps: List[Tuple[AgentAction, str]] = []
    #agent = create_react_agent(llm, tools, prompt_template)
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt_template
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step = None
    max_steps = 10  # Limite al numero massimo di iterazioni
    step_count = 0
    while not isinstance(agent_step, AgentFinish) and step_count < max_steps:
        agent_step = agent.invoke(
            {
                "input": "What is the length of the word: DOG?",
                "agent_scratchpad": intermediate_steps,
            }
        )
        print(type(agent_step))

        #agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        #    {
        #        "input": "What is the length of the word: DOG?",
        #        "agent_scratchpad": intermediate_steps,
        #    }
        #)
        print("########## AGENT STEP: ")
        print(agent_step)
        print("#######################")

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            observation = tool_to_use.func(str(tool_input))
            #print(f"{observation=}")
            intermediate_steps.append((agent_step, str("Observation:", observation)))
            step_count += 1  # Incrementa il contatore di passi

    if isinstance(agent_step, AgentFinish):
        print(agent_step.return_values)
    else:
        print("Max steps reached without reaching a final answer.")
    #agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=5)
    #ai_response = agent_executor.invoke({"input": "What is the length of the word 'DOG' in number of characters?"})
    #print(ai_response)
