
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

@tool
def get_github_issue(args: str) -> str:
    """
    Get an issue of the specified GitHub repository. The function expects the following parameters:
    issue_id (the id of the issue, it must be an integer);
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 1):
      return ("Error: wrong number of arguments. The tool must be called with 1 argument: issue_id."
              "- issue_id must be an integer.\n"
              "Example: issue_id=1.")

    #repo_name = params[0]
    #if not repo_name.strip():
    #    return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    #if '/' not in repo_name or repo_name.count('/') != 1:
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    print(f"Repository: {DEFAULT_REPOSITORY_NAME}")
    print(f"Issue Id: {issue_id}")

    issue = github_client.get_issue(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id)
    return f"Github issue successfully retrieved: {issue.html_url}"

@tool
def get_github_issues_by_assignee(args: str) -> str:
    """
    Get all the issues assigned to an user for the specified GitHub repository. The function expects no parameters.
    The function returns the list of issues URLs.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 0):
      return ("Error: wrong number of arguments. The tool must be called with 0 arguments.")

    #repo_name = params[0]
    #if not repo_name.strip():
    #    return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    #if '/' not in repo_name or repo_name.count('/') != 1:
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    #assignee = params[1]
    # Verifica che assignee non sia vuoto e sia 'sasadangelo'
    #if not assignee.strip():
    #    return "Error: invalid assignee. The parameter cannot be an empty string."

    #if assignee != 'sasadangelo':
    #    assignee='sasadangelo'

    print(f"Repository: {DEFAULT_REPOSITORY_NAME}")
    print(f"Assignee: {DEFAULT_ASSIGNEE}")

    issues_list_paged = github_client.get_issues_by_assignee(repo_name=DEFAULT_REPOSITORY_NAME, assignee=DEFAULT_ASSIGNEE)
    issue_urls = [issue.html_url for issue in issues_list_paged]
    return f"Github issues assigned to the {DEFAULT_ASSIGNEE} user successfully retrieved: {issue_urls}"

@tool
def get_github_issues_by_label(args: str) -> str:
    """
    Get all the issues with the given label for the specified GitHub repository. The function expects no parameters.
    The function returns the list of issues URLs.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 1):
      return ("Error: wrong number of arguments. The tool must be called with 1 arguments: label"
              "- label must be an string.\n"
              "Example: label=onboard.")

    label = params[1]

    if not label.strip():
        return "Error: invalid label. The parameter cannot be an empty string."

    #repo_name = params[0]
    #if not repo_name.strip():
    #    return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    #if '/' not in repo_name or repo_name.count('/') != 1:
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    #assignee = params[1]
    # Verifica che assignee non sia vuoto e sia 'sasadangelo'
    #if not assignee.strip():
    #    return "Error: invalid assignee. The parameter cannot be an empty string."

    #if assignee != 'sasadangelo':
    #    assignee='sasadangelo'

    print(f"Repository: {DEFAULT_REPOSITORY_NAME}")
    print(f"Label: {label}")

    issues_list_paged = github_client.get_issues_by_label(repo_name=DEFAULT_REPOSITORY_NAME, label=label)
    issue_urls = [issue.html_url for issue in issues_list_paged]
    return f"Github issues with label {label} successfully retrieved: {issue_urls}"

@tool
def update_github_issue_status(args: str) -> str:
    """
    Update the issue status of the specified GitHub repository. The function expects the following parameters:
    - issue_id (the id of the issue, it must be an integer);
    - status (the new issue status, it must be a string equal to 'open' or 'close');
    The values of these parameters must be separated by the "|" character.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 2):
        return ("Error: wrong number of arguments. The tool must be called with 2 arguments: issue_id, and status."
                "- 'issue_id' must be an integer.\n"
                "- 'status' must each be a string equal to 'close' or 'open'.\n"
                "The values of these parameters must be separated by the "|" character.\n"
                "Example: issue_id=1, status=close.")

    #repo_name = params[0]
    #if not repo_name.strip():
    #    return "Error: Invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    #if '/' not in repo_name or repo_name.count('/') != 1:
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    status = params[2]
    # Verifica che status sia 'open' o 'close'
    if status not in ["open", "close"]:
        return f"Error: invalid status: '{status}'. It must be either 'open' or 'close'."

    print(f"Repository: {DEFAULT_REPOSITORY_NAME}")
    print(f"Issue Id: {issue_id}")
    print(f"Status: {status}")

    issue = github_client.update_issue_status(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id, status=status)
    return f"Status of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_assignee(args: str) -> str:
    """
    Update an issue assignee of the specified GitHub repository. The function expects the following parameters:
    - issue_id (the id of the issue, it must be an integer);
    The values of these parameters must be separated by the "|" character.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 1):
        return ("Error: wrong number of arguments. The tool must be called with 1 arguments: issue_id.\n"
                "- issue_id, must be an integer.\n"
                "Example: issue_id=1.")

    #repo_name = params[0]
    #if not repo_name.strip():
    #    return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    #if '/' not in repo_name or repo_name.count('/') != 1:
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    #assignee = params[2]
    # Verifica che assignee non sia vuoto e sia 'sasadangelo'
    #if not assignee.strip():
    #    return "Error: invalid assignee. The parameter cannot be an empty string."

    #if assignee != 'sasadangelo':
    #    assignee='sasadangelo'

    print(f"Repository: {DEFAULT_REPOSITORY_NAME}")
    print(f"Issue Id: {issue_id}")
    print(f"Assignee: {DEFAULT_ASSIGNEE}")

    issue = github_client.update_issue_assignee(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id, new_assignee=DEFAULT_ASSIGNEE)
    return f"Assignee of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_body(args: str) -> str:
    """
    Update an issue body of the specified GitHub repository. The function expects the following parameters:
    - issue_id (the id of the issue, it must be an integer);
    - body (the new issue body, it must be a string)
    The values of these parameters must be separated by the "|" character.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 2):
        return ("Error: wrong number of arguments. The tool must be called with 2 arguments: issue_id and body.\n"
                "- issue_id must each be an integer.\n"
                "- body must each be a string.\n"
                "Example: issue_id=1, body='my text body'.\n")

    #repo_name = params[0]
    #if not repo_name.strip():
    #    return "Invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    #if '/' not in repo_name or repo_name.count('/') != 1:
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository'."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    body = params[2]
    if not body.strip():
        return "Error: invalid body. The parameter cannot be an empty string."

    print(f"Repository: {DEFAULT_REPOSITORY_NAME}")
    print(f"Issue Id: {issue_id}")
    print(f"Body: {body}")

    issue = github_client.update_issue_body(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id, new_body=body)
    return f"Body of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_title(args: str) -> str:
    """
    Update the issue title of the specified GitHub repository. The function expects the following parameters:
    - issue_id (the id of the issue, it must be an integer);
    - title (the new issue title, it must be a string)
    The values of these parameters must be separated by the "|" character.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 2):
        return ("Error: wrong number of arguments. The tool must be called with 2 arguments: issue_id and title.\n"
                "- issue_id must each be an integer.\n"
                "- title must each be a string.\n"
                "Example: issue_id=1 and title='my text title'.")

    #repo_name = params[0]
    #if not repo_name.strip():
    #    return "Error: invalid repository name. The parameter cannot be an empty string."

    # Verifica che repo_name sia nella forma user/repo_name
    #if '/' not in repo_name or repo_name.count('/') != 1:
    #    return f"Error: invalid repository name: '{repo_name}'. The parameter must be in the format 'user/repository' with a forward slash."

    try:
        issue_id = int(params[1])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[1]}'. The issue ID must be an integer."

    title = params[2]
    # Verifica che title e body non siano vuoti
    if not title.strip():
        return "Error: invalid title. The parameter cannot be an empty string."

    print(f"Repository: {DEFAULT_REPOSITORY_NAME}")
    print(f"Issue Id: {issue_id}")
    print(f"Title: {title}")

    issue = github_client.update_issue_title(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id, new_title=title)
    return f"Title of the github issue successfully updated: {issue.html_url}"

github_issues_tools=[create_github_issue, get_github_issue, update_github_issue_status, update_github_issue_assignee, update_github_issue_body, update_github_issue_title, get_github_issues_by_assignee]