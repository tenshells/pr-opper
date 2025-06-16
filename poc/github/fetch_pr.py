import os
from github import Auth, Github
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# using an access token
auth = Auth.Token(GITHUB_TOKEN)

# First create a Github instance:
g = Github(auth=auth)

prs = g.get_repo("tenshells/pr-opper").get_pulls()

for pr in prs:
    print(pr.title)

# To close connections after use
g.close()
