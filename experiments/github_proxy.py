import os
from dotenv import load_dotenv
from github import Github, Issue, IssueComment

def create_github_issue(repo_name: str, title: str, body: str, assignee: str) -> Issue:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    return repo.create_issue(title=title, body=body, assignee=assignee)

def get_github_issue(repo_name: str, issue_id: int) -> Issue:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    return repo.get_issue(number=issue_id)

def update_github_issue_status(repo_name: str, issue_id: int, action: str) -> Issue:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_id)
    issue.edit(state=action)
    return issue

def update_github_issue_assignee(repo_name: str, issue_id: int, new_assignee: str) -> Issue:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_id)
    issue.edit(assignee=new_assignee)
    return issue

def update_github_issue_body(repo_name: str, issue_id: int, new_body: str) -> Issue:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_id)
    issue.edit(body=new_body)
    return issue

def add_comment_to_github_issue(repo_name: str, issue_id: int, comment: str) -> IssueComment:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_id)
    return issue.create_comment(comment)

from github import Github, GithubException

def get_all_github_issue_comments_by_page(repo_name: str, issue_id: int, page: int = 1) -> list:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_id)
    return issue.get_comments().get_page(page - 1)

def get_github_issue_comment(repo_name: str, issue_id: int, page: int = 1, position: int = 0) -> IssueComment:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_id)
    comments_paged = issue.get_comments()
    comments_page = comments_paged.get_page(page - 1)
    if 0 <= position < len(comments_page):
        return comments_page[position]

def update_github_issue_comment(repo_name: str, issue_id: int, page: int = 1, position: int = 0, new_body: str = "") -> IssueComment:
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_id)
    comments_paged = issue.get_comments()
    comments_page = comments_paged.get_page(page - 1)
    if 0 <= position < len(comments_page):
        comment = comments_page[position]
        comment.edit(body=new_body)
        return comment

def delete_github_issue_comment(repo_name: str, issue_id: int, page: int = 1, position: int = 0):
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_id)
    comments_paged = issue.get_comments()
    comments_page = comments_paged.get_page(page - 1)
    if 0 <= position < len(comments_page):
        comment = comments_page[position]
        # Cancella il commento
        comment.delete()

def main():
    load_dotenv(".env")
    #issue = create_github_issue(repo_name="sasadangelo/chess", title="my test issue", body="bla bla bla", assignee="sasadangelo")
    update_github_issue_status(repo_name="sasadangelo/chess", issue_id=1, action='close')
    #update_github_issue_assignee(repo_name="sasadangelo/chess", issue_id=1, new_assignee='sasadangelo')
    #update_github_issue_body(repo_name="sasadangelo/chess", issue_id=1, new_body='bla 1 bla 2 bla 3')
    #issue = get_github_issue(repo_name="sasadangelo/chess", issue_id=1)
    #print(issue)
    #issue_comment = add_comment_to_github_issue(repo_name="sasadangelo/chess", issue_id=1, comment="bla bla bla")
    #print(issue_comment)
    #comments = get_all_github_issue_comments_by_page(repo_name="sasadangelo/chess", issue_id=1)
    #for comment in comments:
    #    print(comment)
    #comment = get_github_issue_comment(repo_name="sasadangelo/chess", issue_id=1, page=1, position=0)
    #comment = update_github_issue_comment(repo_name="sasadangelo/chess", issue_id=1, page=1, position=0, new_body="bla 1 bla 2 bla 3 4444")
    #print(comment)
    #delete_github_issue_comment(repo_name="sasadangelo/chess", issue_id=1, page=1, position=0)


if __name__ == "__main__":
    # Call the main function when the script is executed.
    main()

