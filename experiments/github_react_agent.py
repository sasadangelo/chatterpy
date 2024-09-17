from react_agent import ReActAgent
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
#from github_tools import github_issues_tools
from langchain.prompts import PromptTemplate
from github_facade import GitHub
from github import GithubException
from langchain.tools import tool

DEFAULT_REPOSITORY_NAME="sasadangelo/chattery_issue"
DEFAULT_ASSIGNEE="sasadangelo"

# Create an instance of the GitHub class
github_client = GitHub()

def parse_params(args: str) -> str:
    print("ARGS:", args)
    cleaned_args = args.replace('"', '').replace("'", "")
    print("CLEANED ARGS:", cleaned_args)
    params = [param.strip() for param in cleaned_args.split('|') if param.strip()]
    return params


@tool
def create_github_issue(args: str) -> str:
    """
    This tool creates a GitHub issue. The function expects the following parameters:
    - title: the title of the issue, the parameter must be a string;
    - body: the content of the issue, the parameter must be a string;
    - label: the label associated to the issue, the parameter must be a string;
    Try to determine the title, body, and label from the user prompt in this exact order.
    Once you determined these parameters values, pass them to this tool separated by the "|" character.
    The function returns the issue URL.
    """
    print("####################################################################################################")
    params = parse_params(args)
    print(params)

    if (len(params) != 3):
      return ("Error: wrong number of arguments. The tool must be called with 3 arguments: title, body, and label.\n"
              "- title must be a string.\n"
              "- body  must be a string.\n"
              "- label  must be a string.\n"
              "Example: title=Issue title, body=Issue body, label=onboarding.")

    #repo_name = params[0]
    #if not repo_name.strip():
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    #if '/' not in repo_name or repo_name.count('/') != 1:
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    title = params[0]
    body = params[1]
    label = params[2]

    # Verifica che title e body non siano vuoti
    if not title.strip():
        return "Error: invalid title. The parameter cannot be an empty string."

    if not body.strip():
        return "Error: invalid body. The parameter cannot be an empty string."

    if not label.strip():
        return "Error: invalid label. The parameter cannot be an empty string."

    #assignee = params[3]
    # Verifica che assignee non sia vuoto e sia 'sasadangelo'
    #if not assignee.strip():
    #    return "Error: invalid assignee. The parameter cannot be an empty string."

    #if assignee != 'sasadangelo':
    #    assignee='sasadangelo'

    print(f"Creating an issue in the repository: {DEFAULT_REPOSITORY_NAME}, with title:{title}, assigned to {DEFAULT_ASSIGNEE}")

    try:
        issue = github_client.create_issue(repo_name=DEFAULT_REPOSITORY_NAME, title=title, body=body, assignee=DEFAULT_ASSIGNEE, labels=[label])
    except GithubException as e:
        # Gestisci eventuali altre eccezioni generiche
        return f"Error: the issue cannot be created. This is the returned error: {str(e)}"

    return f"Github issue successfully created: {issue.html_url}."

github_issues_tools=[create_github_issue]

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
