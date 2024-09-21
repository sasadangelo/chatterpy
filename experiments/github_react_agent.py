from react_agent import ReActAgent
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import PromptTemplate
from github_facade import GitHub
from github_tools import create_github_issue, get_github_issues_by_label, get_github_issue, update_github_issue_status, update_github_issue_assignee, update_github_issue_body, update_github_issue_title, get_github_issues_by_assignee

DEFAULT_REPOSITORY_NAME="sasadangelo/chattery_issue"
DEFAULT_ASSIGNEE="sasadangelo"

# Create an instance of the GitHub class
github_client = GitHub()

github_issues_tools=[create_github_issue, get_github_issues_by_label, get_github_issue, update_github_issue_status, update_github_issue_assignee, update_github_issue_body, update_github_issue_title, get_github_issues_by_assignee]

class GithubReActAgent(ReActAgent):
    PROMPT_TEMPLATE="""You are a helpful, respectful and honest Github Agent assistant. You can help the user to manage its Github issues in his repositories.
You have access to the following tools to achieve this goal:
{tools}

To answer the question you can use the following process:

Question: the input question you must answer
Thought: you should always think about what to do, usually it is something related to GitHub issues (i.e. create an issue, update an issue status, etc.)
Action: the action to take, usually it is a tool execution and it should be one of the following tools [{tool_names}]. Don't use backticks around the tool name.
Action Input: the input to the action. It is a list of parameters separated by the "|" character. If you have only one parameter don't add the separator "|".
Observation: always analyze the result of the action of the tool. If the tool return a string with the words "successfully" or "error" it means its execution is completed and you should observe (analyze) a possible next action to take or think to the Final Answer.
... (the flow Thought/Action/Action Input/Observation could repeat max N time until you find the Final Answer)
Thought: I now know the Final Answer and I prepare the right output to show to the user.
Final Answer: the final answer to the original input question.

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

    def __init__(self, llm: BaseChatModel, verbose: bool = True, handle_parsing_errors=True):
        prompt_template = PromptTemplate.from_template(GithubReActAgent.PROMPT_TEMPLATE)
        super().__init__(llm, github_issues_tools, prompt_template, verbose, handle_parsing_errors)

    def invoke(self, user_input: str) -> dict[str, Any]:
        return super().invoke(user_input)
