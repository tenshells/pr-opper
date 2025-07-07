import os
import re
from dotenv import load_dotenv
from github import Auth, Github, GithubException, UnknownObjectException
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
auth = Auth.Token(GITHUB_TOKEN)

def single_comment_on_pr(repo, pr_number, token, commit_sha, position, path, comment):
    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
        username = g.get_user().login
        pr = g.get_repo(f"{username}/{repo}").get_pull(pr_number)
        commit = g.get_repo(f"{username}/{repo}").get_commit(commit_sha)
        print("adding comment: ", comment)
        pr.create_comment(
            body=comment,
            commit=commit,
            position=position,
            path=path
        )
    except UnknownObjectException as e:
        print(f"Make sure input repo, pr number is correct... {e}")
    except Exception as e:
        print(f"Something went wrong... {e}")

repo = "pr-opper"
pull_request_number = 2
position = 1
path = "poc/github/fetch_pr.py"
commit_sha = "22ad7f2464db9b3f21da68719565dd82a5f381f6"
comment = "This is 7th comment, creating commit from sha.."

# single_comment_on_pr(repo, 
#                     pull_request_number, 
#                     GITHUB_TOKEN, 
#                     commit_sha, 
#                     position, 
#                     path, 
#                     comment)

# static: repo, pr number, gh token, 
# dynamic: commit, position, path, comment
