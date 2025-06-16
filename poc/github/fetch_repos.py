import os
from github import Github

# Authentication is defined via github.Auth
from github import Auth
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# using an access token
auth = Auth.Token(GITHUB_TOKEN)

# First create a Github instance:
g = Github(auth=auth)

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)

# To close connections after use
g.close()