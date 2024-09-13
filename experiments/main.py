from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
# from github_tools import github_tools
from github_facade import GitHub
from langchain.tools import tool
from github import GithubException

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
    Create an issue in the specified GitHub repository. The function expects the following parameters:
    repo_name (the name of the repository, it must be a string in the format of user/repo_name with a forward slash);
    title (the title of the issue, the parameter must be a string);
    body (the content of the issue, the parameter must be a string);
    assignee (the GitHub username to assign the issue to).
    The values of these parameters must be comma-separated and without single or double quotes.
    The function returns the issue URL.
    """
    print("####################################################################################################")
    params = parse_params(args)
    print(params)

    if (len(params) != 4):
      return ("Error: wrong number of arguments. The tool must be called with 4 arguments: "
              "repository name, title, body, and assignee. The parameters must be "
              "comma-separated and without single or double quotes.\n"
              "- 'repository name' must be a string in the format 'user/repository' with a forward slash.\n"
              "- 'title', 'body', and 'assignee' must each be strings.\n"
              "Example: repo_name=user/repository, title=Issue title, body=Issue body, assignee=username.")

    repo_name = params[0]
    if not repo_name.strip():
        return f"Error: invalid repository name: '{repo_name}'. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    if '/' not in repo_name or repo_name.count('/') != 1:
        return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    title = params[1]
    body = params[2]

    # Verifica che title e body non siano vuoti
    if not title.strip():
        return "Error: invalid title. The parameter cannot be an empty string."

    if not body.strip():
        return "Error: invalid body. The parameter cannot be an empty string."

    assignee = params[3]
    # Verifica che assignee non sia vuoto e sia 'sasadangelo'
    if not assignee.strip():
        return "Error: invalid assignee. The parameter cannot be an empty string."

    if assignee != 'sasadangelo':
        assignee='sasadangelo'

    print(f"Creating an issue in the repository: {repo_name}, with title:{title}, assigned to {assignee}")

    try:
        issue = github_client.create_issue(repo_name=repo_name, title=title, body=body, assignee=assignee)
    except GithubException as e:
        # Gestisci eventuali altre eccezioni generiche
        return f"Error: the issue cannot be created. This is the returned error: {str(e)}"

    return f"Github issue successfully created: {issue.html_url}."

@tool
def get_github_issue(args: str) -> str:
    """
    Get an issue of the specified GitHub repository. The function expects the following parameters:
    repo_name (the name of the repository, it must be a string in the formt of user/repo_name with a forward slash);
    issue_id (the id of the issue, it must be an integer);
    The values of these parameters must be comma-separated and without single or double quotes.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 2):
      return ("Error: wrong number of arguments. The tool must be called with 2 arguments: "
              "repository name, issue_id. The parameters must be comma-separated and without single or double quotes.\n"
              "- 'repository name' must be a string in the format 'user/repository' with a forward slash.\n"
              "- 'issue_id' must be an integer.\n"
              "Example: repo_name=user/repository, issue_id=1.")

    repo_name = params[0]
    if not repo_name.strip():
        return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    if '/' not in repo_name or repo_name.count('/') != 1:
        return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    print(f"Repository: {repo_name}")
    print(f"Issue Id: {issue_id}")

    issue = github_client.get_issue(repo_name=repo_name, issue_id=issue_id)
    return f"Github issue successfully retrieved: {issue.html_url}"

@tool
def get_github_issues_by_assignee(args: str) -> str:
    """
    Get all the issues assigned to an user for the specified GitHub repository. The function expects the following parameters:
    repo_name (the name of the repository, it must be a string in the format of user/repo_name with a forward slash);
    assignee (the assignee of the issues, it must be a string);
    The values of these parameters must be comma-separated and without single or double quotes.
    The function returns the list of issues URLs.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 2):
      return ("Error: wrong number of arguments. The tool must be called with 2 arguments: "
              "repository name, assignee. The parameters must be comma-separated and without single or double quotes.\n"
              "- 'repository name' must be a string in the format 'user/repository' with a forward slash.\n"
              "- 'assignee' must each be a string.\n"
              "Example: repo_name=user/repository, assignee=username.")

    repo_name = params[0]
    if not repo_name.strip():
        return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    if '/' not in repo_name or repo_name.count('/') != 1:
        return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    assignee = params[1]
    # Verifica che assignee non sia vuoto e sia 'sasadangelo'
    if not assignee.strip():
        return "Error: invalid assignee. The parameter cannot be an empty string."

    if assignee != 'sasadangelo':
        assignee='sasadangelo'

    print(f"Repository: {repo_name}")
    print(f"Assignee: {assignee}")

    issues_list_paged = github_client.get_issues_by_assignee(repo_name=repo_name, assignee=assignee)
    issue_urls = [issue.html_url for issue in issues_list_paged]
    return f"Github issues assigned to the {assignee} user successfully retrieved: {issue_urls}"

@tool
def update_github_issue_status(args: str) -> str:
    """
    Update the issue status of the specified GitHub repository. The function expects the following parameters:
    repo_name (the name of the repository, it must be a string in the format of user/repo_name with a forward slash);
    issue_id (the id of the issue, it must be an integer);
    status (the new issue status, it must be a string equal to 'open' or 'close')
    The values of these parameters must be comma-separated and without single or double quotes.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 3):
        return ("Error: wrong number of arguments. The tool must be called with 3 arguments: "
                "repository name, issue_id, and status. The parameters must be "
                "comma-separated and without single or double quotes.\n"
                "- 'repository name' must be a string in the format 'user/repository' with a forward slash.\n"
                "- 'issue_id' must be an integer.\n"
                "- 'status' must each be a string equal to 'close' or 'open'.\n"
                "Example: repo_name=user/repository, issue_id=1, status=close.")

    repo_name = params[0]
    if not repo_name.strip():
        return "Error: Invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    if '/' not in repo_name or repo_name.count('/') != 1:
        return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    status = params[2]
    # Verifica che status sia 'open' o 'close'
    if status not in ["open", "close"]:
        return f"Error: invalid status: '{status}'. It must be either 'open' or 'close'."

    print(f"Repository: {repo_name}")
    print(f"Issue Id: {issue_id}")
    print(f"Status: {status}")

    issue = github_client.update_issue_status(repo_name=repo_name, issue_id=issue_id, status=status)
    return f"Status of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_assignee(args: str) -> str:
    """
    Update an issue assignee of the specified GitHub repository. The function expects the following parameters:
    repo_name (the name of the repository, it must be a string in the format of user/repo_name with a forward slash);
    issue_id (the id of the issue, it must be an integer);
    assignee (the new issue assignee, it must be a string)
    The values of these parameters must be comma-separated and without single or double quotes.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 3):
        return ("Error: wrong number of arguments. The tool must be called with 3 arguments: "
                "repository name, title, body, and assignee. The parameters must be "
                "comma-separated and without single or double quotes.\n"
                "- 'repository name' must be a string in the format 'user/repository' with a forward slash.\n"
                "- 'issue_id' must each be an integer.\n"
                "- 'assignee' must each be a string.\n"
                "Example: repo_name=user/repository, issue_id=1, assignee=username.")

    repo_name = params[0]
    if not repo_name.strip():
        return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    if '/' not in repo_name or repo_name.count('/') != 1:
        return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    assignee = params[2]
    # Verifica che assignee non sia vuoto e sia 'sasadangelo'
    if not assignee.strip():
        return "Error: invalid assignee. The parameter cannot be an empty string."

    if assignee != 'sasadangelo':
        assignee='sasadangelo'

    print(f"Repository: {repo_name}")
    print(f"Issue Id: {issue_id}")
    print(f"Assignee: {assignee}")

    issue = github_client.update_issue_assignee(repo_name=repo_name, issue_id=issue_id, new_assignee=assignee)
    return f"Assignee of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_body(args: str) -> str:
    """
    Update an issue body of the specified GitHub repository. The function expects the following parameters:
    repo_name (the name of the repository, it must be a string in the format of user/repo_name with a forward slash);
    issue_id (the id of the issue, it must be an integer);
    body (the new issue body, it must be a string)
    The values of these parameters must be comma-separated and without single or double quotes.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 3):
        return ("Error: wrong number of arguments. The tool must be called with 3 arguments: "
                "repository name, issue_id, body. The parameters must be "
                "comma-separated and without single or double quotes.\n"
                "- 'repository name' must be a string in the format 'user/repository' with a forward slash.\n"
                "- 'issue_id' must each be an integer.\n"
                "- 'body' must each be a string.\n"
                "Example: repo_name=user/repository, issue_id=1, body='my text body'.")

    repo_name = params[0]
    if not repo_name.strip():
        return "Invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    if '/' not in repo_name or repo_name.count('/') != 1:
        return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository'."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    body = params[2]
    if not body.strip():
        return "Error: invalid body. The parameter cannot be an empty string."

    print(f"Repository: {repo_name}")
    print(f"Issue Id: {issue_id}")
    print(f"Body: {body}")

    issue = github_client.update_issue_body(repo_name=repo_name, issue_id=issue_id, new_body=body)
    return f"Body of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_title(args: str) -> str:
    """
    Update the issue title of the specified GitHub repository. The function expects the following parameters:
    repo_name (the name of the repository, it must be a string in the format of user/repo_name with a forward slash);
    issue_id (the id of the issue, it must be an integer);
    title (the new issue title, it must be a string)
    The values of these parameters must be comma-separated and without single or double quotes.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 3):
        return ("Error: wrong number of arguments. The tool must be called with 3 arguments: "
                "repository name, issue_id, title. The parameters must be "
                "comma-separated and without single or double quotes.\n"
                "- 'repository name' must be a string in the format 'user/repository' with a forward slash.\n"
                "- 'issue_id' must each be an integer.\n"
                "- 'title' must each be a string.\n"
                "Example: repo_name=user/repository, issue_id=1, title='my text title'.")

    repo_name = params[0]
    if not repo_name.strip():
        return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    if '/' not in repo_name or repo_name.count('/') != 1:
        return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    title = params[2]
    # Verifica che title e body non siano vuoti
    if not title.strip():
        return "Error: invalid title. The parameter cannot be an empty string."

    print(f"Repository: {repo_name}")
    print(f"Issue Id: {issue_id}")
    print(f"Title: {title}")

    issue = github_client.update_issue_title(repo_name=repo_name, issue_id=issue_id, new_title=title)
    return f"Title of the github issue successfully updated: {issue.html_url}"

github_issues_tools=[create_github_issue, get_github_issue, update_github_issue_status, update_github_issue_assignee, update_github_issue_body, update_github_issue_title, get_github_issues_by_assignee]

model_name = "llama3"
base_url = "http://localhost:11434"

def get_react_prompt_template():
    return PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:
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
        agent = create_react_agent(llm, github_issues_tools, prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=github_issues_tools, verbose=True, handle_parsing_errors=True, max_iterations=5)
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