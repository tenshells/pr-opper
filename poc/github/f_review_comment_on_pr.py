import os
from github import Auth, Github
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# using an access token


def review_comment_on_pr(repo, pull_request_number, GITHUB_TOKEN, review_comment):
    # First create a Github instance:
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)
    username = g.get_user().login
    pr = g.get_repo(f"{username}/{repo}").get_pull(pull_request_number)
    print("adding review comment: ", review_comment)
    pr.create_review(
        body=review_comment,
    )
    # To close connections after use
    g.close()

# review_comment_on_pr("pr-opper", 2, GITHUB_TOKEN, "This is third comment, second comment was created with create_review with the message in body..")

