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
    pr.create_review(
        body="This is third comment, second comment was created with create_review with the message in body..", 
        # commit=pr.get_commits()[0]
    )
# To close connections after use
g.close()
