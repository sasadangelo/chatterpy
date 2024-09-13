from react_agent import ReActAgent
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from github_tools import github_issues_tools
from langchain.prompts import PromptTemplate

class GithubReActAgent(ReActAgent):
    PROMPT_TEMPLATE="""You are a helpful, respectful and honest Github Agent assistant. You can help the user to manage the issues in his repositories.
You have access to the following tools to achieve this goal:
{tools}

To answer the question you can use the following format:

Question: the input question you must answer
Thought: you should always think about what to do, usually it is something related to GitHub issues (i.e. create an issue, update an issue status, etc.)
Action: the action to take, should be one of the following tools [{tool_names}]. Don't use backticks around the tool name.
Action Input: the input to the action. It is a list of parameters separated by the "|" character.
Observation: the result of the action. If the action is successfully or an error occurred exit immediately with the result for the user.
... (only in the case of multiple actions requested by the user this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer and I prepare the right output to show to the user.
Final Answer: the final answer to the original input question.

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

    def __init__(self, llm: BaseChatModel, verbose: bool = True, handle_parsing_errors=True):
        prompt_template = PromptTemplate.from_template(GithubReActAgent.PROMPT_TEMPLATE)
        super().__init__(llm, github_issues_tools, prompt_template, verbose, handle_parsing_errors)

    def invoke(self, user_input: str) -> dict[str, Any]:
        return super().invoke(user_input)
