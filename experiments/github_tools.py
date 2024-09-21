
from langchain.tools import tool
from github import GithubException
from github_facade import GitHub

DEFAULT_REPOSITORY_NAME="sasadangelo/chattery_issue"
DEFAULT_ASSIGNEE="sasadangelo"

# Create an instance of the GitHub class
github_client = GitHub()

def parse_params(args: str) -> str:
    print("ARGS:", args)
    cleaned_args = args.replace('"', '').replace("'", "")
    print("CLEANED ARGS:", cleaned_args)
    params = [param.strip() for param in cleaned_args.split('|') if param.strip()]

    # Exclude words
    exclude_words = {"title", "body", "label"}

    # Remove undesired words
    filtered_params = [param for param in params if param not in exclude_words]

    return filtered_params


@tool
def create_github_issue(args: str) -> str:
    """
    This tool creates a GitHub issue. The function expects 3 parameters:
    - the title of the issue, the parameter must be a string;
    - the body (content) of the issue, the parameter must be a string;
    - the label associated to the issue, the parameter must be a string and a single word;
    The values of these parameters must be separated by "|" character and without single or double quotes.
    The function returns the issue URL.
    """
    print("\n####################################################################################################")
    params = parse_params(args)
    print(params)

    if (len(params) != 3):
      return ("Error: wrong number of parameters. The tool must be called with 3 parameters: title, body, and label.\n"
              "- title must be a string.\n"
              "- body  must be a string.\n"
              "- label  must be a string.\n"
              "Example: issue title|issue body|onboarding.")

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

    if len(label.split()) > 1:
        return "Error: invalid label. The parameter must be a single word."

    try:
        issue = github_client.create_issue(repo_name=DEFAULT_REPOSITORY_NAME, title=title, body=body, assignee=DEFAULT_ASSIGNEE, label=label)
    except GithubException as e:
        # Gestisci eventuali altre eccezioni generiche
        return f"Error: the issue cannot be created. This is the returned error: {str(e)}"

    return f"Github issue successfully created: {issue.html_url}."

@tool
def get_github_issue(args: str) -> str:
    """
    Get an issue of the specified GitHub repository. The function expects 1 parameter:
    - issue_id: the id of the issue, it must be an integer;
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 1):
      return ("Error: wrong number of parameters. The tool must be called with 1 parameter: issue_id."
              "- issue_id must be an integer.\n"
              "Example: issue_id=1.")

    try:
        issue_id = int(params[0])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{params[0]}'. The issue ID must be an integer."

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

    issues_list_paged = github_client.get_issues_by_assignee(repo_name=DEFAULT_REPOSITORY_NAME, assignee=DEFAULT_ASSIGNEE)
    issue_urls = [issue.html_url for issue in issues_list_paged]
    return f"Github issues assigned to the {DEFAULT_ASSIGNEE} user successfully retrieved: {issue_urls}"

@tool
def get_github_issues_by_label(args: str) -> str:
    """
    Get all the issues with the given label for the specified GitHub repository. The function expects 1 parameter:
    - label: the label associated to the issue, the parameter must be a string and a single word;
    The function returns the list of issues URLs.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 1):
      return ("Error: wrong number of arguments. The tool must be called with 1 arguments: label"
              "- label must be an string and a single word.\n"
              "Example: label=onboard.")

    label = params[0]

    if not label.strip():
        return "Error: invalid label. The parameter cannot be an empty string."

    print(f"Label: {label}")

    issues_list_paged = github_client.get_issues_by_tag(repo_name=DEFAULT_REPOSITORY_NAME, tag=label)
    issue_urls = [issue.html_url for issue in issues_list_paged]
    return f"Github issues with label {label} successfully retrieved: {issue_urls}"

@tool
def update_github_issue_status(args: str) -> str:
    """
    Update the issue status of the specified GitHub repository. The function expects 2 parameters:
    - issue_id: the id of the issue, it must be an integer;
    - status: the new issue status, it must be a string equal to 'open' or 'close';
    The values of these parameters must be separated by "|" character and without single or double quotes.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 2):
        return ("Error: wrong number of arguments. The tool must be called with 2 arguments: issue_id, and status."
                "- issue_id must be an integer.\n"
                "- status must each be a string equal to 'close' or 'open'.\n"
                "The values of these parameters must be separated by the "|" character.\n"
                "Example: issue_id=1, status=close.")

    try:
        issue_id = int(params[0])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{issue_id}'. The issue ID must be an integer."

    status = params[1]
    # Verifica che status sia 'open' o 'close'
    if status not in ["open", "close"]:
        return f"Error: invalid status: '{status}'. It must be either 'open' or 'close'."

    print(f"Issue Id: {issue_id}")
    print(f"Status: {status}")

    issue = github_client.update_issue_status(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id, status=status)
    return f"Status of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_assignee(args: str) -> str:
    """
    Update an issue assignee of the specified GitHub repository. The function expects 1 parameter:
    - issue_id: the id of the issue, it must be an integer;
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 1):
        return ("Error: wrong number of arguments. The tool must be called with 1 arguments: issue_id.\n"
                "- issue_id, must be an integer.\n"
                "Example: issue_id=1.")

    try:
        issue_id = int(params[0])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{issue_id}'. The issue ID must be an integer."

    print(f"Issue Id: {issue_id}")

    issue = github_client.update_issue_assignee(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id, new_assignee=DEFAULT_ASSIGNEE)
    return f"Assignee of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_body(args: str) -> str:
    """
    Update an issue body of the specified GitHub repository. The function expects 2 parameters:
    - issue_id: the id of the issue, it must be an integer;
    - body: the new issue body, it must be a string;
    The values of these parameters must be separated by "|" character and without single or double quotes.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 2):
        return ("Error: wrong number of arguments. The tool must be called with 2 arguments: issue_id and body.\n"
                "- issue_id must each be an integer.\n"
                "- body must each be a string.\n"
                "Example: issue_id=1, body='my text body'.\n")

    try:
        issue_id = int(params[0])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{issue_id}'. The issue ID must be an integer."

    body = params[1]
    if not body.strip():
        return "Error: invalid body. The parameter cannot be an empty string."

    print(f"Issue Id: {issue_id}")
    print(f"Body: {body}")

    issue = github_client.update_issue_body(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id, new_body=body)
    return f"Body of the github issue successfully updated: {issue.html_url}"

@tool
def update_github_issue_title(args: str) -> str:
    """
    Update the issue title of the specified GitHub repository. The function expects 2 parameters:
    - issue_id: the id of the issue, it must be an integer;
    - title: the new issue title, it must be a string;
    The values of these parameters must be separated by "|" character and without single or double quotes.
    The function returns the issue URL.
    """
    params = parse_params(args)
    print(params)

    if (len(params) != 2):
        return ("Error: wrong number of arguments. The tool must be called with 2 arguments: issue_id and title.\n"
                "- issue_id must each be an integer.\n"
                "- title must each be a string.\n"
                "Example: issue_id=1 and title='my text title'.")

    try:
        issue_id = int(params[0])  # Tenta di convertire l'ID in un intero
    except ValueError:
        return f"Error: invalid issue ID: '{issue_id}'. The issue ID must be an integer."

    title = params[1]
    # Verifica che title e body non siano vuoti
    if not title.strip():
        return "Error: invalid title. The parameter cannot be an empty string."

    print(f"Issue Id: {issue_id}")
    print(f"Title: {title}")

    issue = github_client.update_issue_title(repo_name=DEFAULT_REPOSITORY_NAME, issue_id=issue_id, new_title=title)
    return f"Title of the github issue successfully updated: {issue.html_url}"
