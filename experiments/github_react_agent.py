from react_agent import ReActAgent
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from github_tools import github_issues_tools
from langchain.prompts import PromptTemplate

class GithubReActAgent(ReActAgent):
    PROMPT_TEMPLATE="""Answer the following questions as best you can. You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action. Use the character "|" to separate the parameters.
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

    def __init__(self, llm: BaseChatModel, verbose: bool = True, handle_parsing_errors=True):
        prompt_template = PromptTemplate.from_template(GithubReActAgent.PROMPT_TEMPLATE)
        super().__init__(llm, github_issues_tools, prompt_template, verbose, handle_parsing_errors)

    def invoke(self, user_input: str) -> dict[str, Any]:
        return super().invoke(user_input)
