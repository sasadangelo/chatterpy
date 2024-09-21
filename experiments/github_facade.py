import os
from typing import List
from dotenv import load_dotenv
from github.Issue import Issue
from github.IssueComment import IssueComment
from github.MainClass import Github
from github.GithubException import BadCredentialsException, UnknownObjectException

class GitHub:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv(".env")
            cls._instance = super(GitHub, cls).__new__(cls)
            github_token = os.environ['GITHUB_TOKEN']
            cls._instance.github_client = Github(github_token)
            cls._instance.repo_cache = {}
        return cls._instance

    def __get_repository(self, repo_name: str):
        if repo_name not in self.repo_cache:
            self.repo_cache[repo_name] = self.github_client.get_repo(repo_name)
        return self.repo_cache[repo_name]

    def create_issue(self, repo_name: str, title: str, body: str, assignee: str, label: str) -> List[Issue]:
        repo = self.__get_repository(repo_name)
        return repo.create_issue(title=title, body=body, assignee=assignee, labels=[label])

    def get_issue(self, repo_name: str, issue_id: int) -> Issue:
        repo = self.__get_repository(repo_name)
        return repo.get_issue(number=issue_id)

    def get_issues_by_assignee(self, repo_name: str, assignee: str) -> Issue:
        repo = self.__get_repository(repo_name)
        issues_list_paged = repo.get_issues(assignee=assignee)
        return list(issues_list_paged)

    def get_issues_by_tag(self, repo_name: str, tag: str) -> List[Issue]:
        repo = self.__get_repository(repo_name)
        issues_list_paged = repo.get_issues(labels=[tag])
        return list(issues_list_paged)

    def update_issue_status(self, repo_name: str, issue_id: int, status: str) -> Issue:
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        issue.edit(state=status)
        return issue

    def update_issue_assignee(self, repo_name: str, issue_id: int, new_assignee: str) -> Issue:
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        issue.edit(assignee=new_assignee)
        return issue

    def update_issue_body(self, repo_name: str, issue_id: int, new_body: str) -> Issue:
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        issue.edit(body=new_body)
        return issue

    def update_issue_title(self, repo_name: str, issue_id: int, new_title: str) -> Issue:
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        issue.edit(title=new_title)
        return issue

    def add_comment(self, repo_name: str, issue_id: int, comment: str) -> IssueComment:
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        return issue.create_comment(comment)

    def get_comments_by_page(self, repo_name: str, issue_id: int, page: int = 1) -> list:
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        return issue.get_comments().get_page(page - 1)

    def get_comment(self, repo_name: str, issue_id: int, page: int = 1, position: int = 0) -> IssueComment:
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        comments_paged = issue.get_comments()
        comments_page = comments_paged.get_page(page - 1)
        if 0 <= position < len(comments_page):
            return comments_page[position]

    def update_comment(self, repo_name: str, issue_id: int, page: int = 1, position: int = 0, new_body: str = "") -> IssueComment:
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        comments_paged = issue.get_comments()
        comments_page = comments_paged.get_page(page - 1)
        if 0 <= position < len(comments_page):
            comment = comments_page[position]
            comment.edit(body=new_body)
            return comment

    def delete_comment(self, repo_name: str, issue_id: int, page: int = 1, position: int = 0):
        repo = self.__get_repository(repo_name)
        issue = repo.get_issue(number=issue_id)
        comments_paged = issue.get_comments()
        comments_page = comments_paged.get_page(page - 1)
        if 0 <= position < len(comments_page):
            comment = comments_page[position]
            comment.delete()

def main():
    load_dotenv(".env")
    try:
        git = GitHub()
        #issue = git.get_issue(repo_name="sasadangelo/chess", issue_id=1)
        #print(issue)
        # issue = git.create_issue(repo_name="sasadangelo/chess", title="my test issue", body="bla bla bla", assignee="sasadangelo")
        #git.update_issue_status(repo_name="sasadangelo/chess", issue_id=2, action='close')
        # git.update_issue_assignee(repo_name="sasadangelo/chess", issue_id=1, new_assignee='sasadangelo')
        #git.update_issue_body(repo_name="sasadangelo/chess", issue_id=1, new_body='Updated body text')
        # git.update_issue_title(repo_name="sasadangelo/chess", issue_id=1, new_title='My new Title')
        # comment = git.add_comment(repo_name="sasadangelo/chess", issue_id=1, comment="This is a new comment")
        # comments = git.get_comments_by_page(repo_name="sasadangelo/chess", issue_id=1)
        #print(comments)
        #comment = git.get_comment(repo_name="sasadangelo/chess", issue_id=1, page=2, position=0)
        #print(comment)
        #comment = git.update_comment(repo_name="sasadangelo/chess", issue_id=1, page=1, position=0, new_body="Updated comment text 222")
        #print(comment)
        #git.delete_comment(repo_name="sasadangelo/chess", issue_id=1, page=1, position=0)
        issue_list=git.get_issues_by_assignee(repo_name="sasadangelo/chattery_issue", assignee="sasadangelo")
        print(issue_list)
    except BadCredentialsException as e:
        print(f"Bad token credentials. Make sure you have the GITHUB_TOKEN variable defined in the .env file.")
    except UnknownObjectException as e:
        print(f"L'oggetto richiesto non esiste.")
    except Exception as e:
        # Cattura l'eccezione generica
        print(f"Si è verificata un'eccezione: {e}")
        print(f"Tipo di eccezione: {type(e).__name__}")
        # Stampa il traceback per ulteriori dettagli
        #traceback.print_exc()    # Example usage:

if __name__ == "__main__":
    main()
