from typing import Any
from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.agents import create_react_agent, AgentExecutor
from agent import Agent

class ReActAgent(Agent):
    def __init__(self, llm: BaseChatModel, tools: list[Callable[..., str]], prompt_template, verbose: bool = True, handle_parsing_errors=True):
        super().__init__(llm, tools, verbose, handle_parsing_errors)
        self.agent = create_react_agent(llm=llm, tools=tools, prompt=prompt_template)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=verbose, handle_parsing_errors=handle_parsing_errors)

    def invoke(self, user_input: str) -> dict[str, Any]:
        return self.agent_executor.invoke(user_input)
