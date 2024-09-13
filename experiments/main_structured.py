from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from github_tools import github_tools
from github_facade import GitHub
from langchain.tools import tool
from github import GithubException
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# Create an instance of the GitHub class
github_client = GitHub()

def validate_repo_name(repo_name: str) -> str | None:
    repo_name = repo_name.strip()
    if not repo_name:
        return f"Error: invalid repository name: '{repo_name}'. The parameter cannot be an empty string."
    if '/' not in repo_name or repo_name.count('/') != 1:
        return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."
    return None

def validate_title(title: str) -> str | None:
    if not title.strip():
        return "Error: invalid title. The parameter cannot be an empty string."
    return None

def validate_body(body: str) -> str | None:
    if not body.strip():
        return "Error: invalid body. The parameter cannot be an empty string."
    return None

def validate_assignee(assignee: str) -> str | None:
    if not assignee.strip():
        return "Error: invalid assignee. The parameter cannot be an empty string."
    return None

class CreateGithubIssueInput(BaseModel):
    repo_name: str = Field(description="the name of the repository, the parameter must be a string in the format of user/repo_name with a forward slash")
    title: str = Field(description="the title of the issue, the parameter must be a string")
    body: str = Field(description="the content of the issue, the parameter must be a string")
    assignee: str = Field(description="the GitHub username to assign the issue to")

class CreateGithubIssueTool(BaseTool):
    name = "create_github_issue"
    description = """
    Create an issue in the specified GitHub repository. The function expects the following parameters:

    - repo_name: The name of the repository. It must be a string in the format 'user/repo_name' with a forward slash.
    - title: The title of the issue. It must be a string.
    - body: The content of the issue. It must be a string.
    - assignee: The GitHub username to assign the issue to.

    The values of these parameters must be comma-separated and without single or double quotes.

    The function returns the issue URL.
    """
    args_schema: Type[BaseModel] = CreateGithubIssueInput

    def _run(self, repo_name: str, title: str, body: str, assignee: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tool."""
        print("11111")
        error = validate_repo_name(repo_name)
        if error:
            return error
        error = validate_title(title)
        if error:
            return error
        error = validate_body(body)
        if error:
            return error
        error = validate_assignee(assignee)
        if error:
            return error
        if assignee != 'sasadangelo':
            assignee='sasadangelo'

        print(f"Creating an issue in the repository: {repo_name}, with title:{title}, assigned to {assignee}")

        try:
            issue = github_client.create_issue(repo_name=repo_name, title=title, body=body, assignee=assignee)
        except GithubException as e:
            # Gestisci eventuali altre eccezioni generiche
            return f"Error: the issue cannot be created. This is the returned error: {str(e)}"

        return f"Github issue successfully created: {issue.html_url}."

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("create_github_issue does not support async")

create_github_issue = CreateGithubIssueTool()


github_tools=[create_github_issue]

model_name = "llama3.1"
base_url = "http://localhost:11434"

def get_react_prompt_template():
    return PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: repo_name, title, body, assignee
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

load_dotenv(".env")
# Inizializza il modello OpenAI
llm = ChatOllama(model=model_name, base_url=base_url)

system_message = """
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.
    Please ensure that your responses are socially unbiased and positive in nature.
    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
    If you don't know the answer to a question, please don't share false information.
    """

#query = (
#    "Create a single issue in the repository sasadangelo/chattery_issue with the following details: "
#    "- Title: Bug in the End Game Gym; "
#    "- Body: The bug is related to the Start Game button that is disabled; "
#    "- Assignee: sasadangelo. "
#)

#query = (
#    "Can you give me the issue 1 in the repository sasadangelo/chattery_issue? "
#)

#query = (
#    "Can you give me all the issues assigned to the sasadangelo user for the sasadangelo/chattery_issue repository? "
#)

# query = (
#     "Can you close the issue 1 in the sasadangelo/chattery_issue repository? "
# )

# Initialize the messages list
messages = [{"role": "system", "content": system_message}]

try:
    while True:
        # Input from the user
        query = input("You: ")
        #query.replace("/", "////")
        #print(query)

        # Add the user message to the conversation
        user_message = {"role": "user", "content": query}
        messages.append(user_message)

        prompt_template = get_react_prompt_template()
        agent = create_react_agent(llm, github_tools, prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=github_tools, verbose=True, handle_parsing_errors=True, max_iterations=3)
        ai_response = agent_executor.invoke({"input": query})

        # Add the AI reply to the conversation
        ai_message = {"role": "assistant", "content": ai_response['output']}
        messages.append(ai_message)

        # Print the AI reply
        print(f"Assistant: {ai_response['output']}")
except EOFError:
    # Terminate the conversation when the user press CTRL-D
    print("\nBye.")


#query = (
#     "Can you change the title of the issue 1 in the sasadangelo/chattery_issue repository specifying that the problem is in the Start Play button of an End? "
#)

#prompt_template = get_react_prompt_template()
#tools=[create_github_issue,get_github_issue,update_github_issue_status,update_github_issue_assignee,update_github_issue_body,update_github_issue_title,get_github_issues_by_assignee]
#agent = create_react_agent(llm, tools, prompt_template)
#agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
#result = agent_executor.invoke({"input": query})
#print(result)