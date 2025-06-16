import os
from github import Auth, Github
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# using an access token
auth = Auth.Token(GITHUB_TOKEN)

# First create a Github instance:
g = Github(auth=auth)
username = g.get_user().login
prs = g.get_repo(f"{username}/pr-opper").get_pulls()

for pr in prs:
    print(pr)
    print(pr.title)
    print(pr.body)
    print(pr.state)
    print(pr.user.login)
    print(pr.created_at, pr.updated_at, pr.closed_at, pr.merged_at)
    print(pr.base.ref)
    print()
    for commit in pr.get_commits():
        print(commit, commit.commit, commit.commit.message)
    for file in pr.get_files():
        print(file.filename, file.status, file.patch)
# To close connections after use
g.close()
