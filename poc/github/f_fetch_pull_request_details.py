import os
from github import Auth, Github
from dotenv import load_dotenv
from models.pull_request_details import ShelCommits, PullRequestDetails

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_pull_request_details(repo, pr_number):
    # using an access token
    auth = Auth.Token(GITHUB_TOKEN)

    # First create a Github instance:
    g = Github(auth=auth)
    username = g.get_user().login
    pr = g.get_repo(f"{username}/{repo}").get_pull(pr_number)

    commits = []
    for commit in pr.get_commits():
        commits.append(ShelCommits(sha=commit.sha, message=commit.commit.message))
    pull_request_details = PullRequestDetails(
        title=pr.title,
        body=pr.body,
        state=pr.state,
        user=pr.user.login,
        created_at=pr.created_at,
        updated_at=pr.updated_at,
        closed_at=pr.closed_at,
        merged_at=pr.merged_at,
        base_ref=pr.base.ref,
        commits=commits
    )
    return pull_request_details

# print(fetch_pull_request_details("pr-opper", 2))
