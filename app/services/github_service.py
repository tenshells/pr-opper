from typing import Dict, Any, Optional
import os
from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository
from github.GithubException import GithubException

class GitHubService:
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub service with token."""
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable or pass token to constructor.")
        self.github = Github(self.token)

    def get_pr_data(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """Get PR data including title, description, and files changed."""
        try:
            # Get repository
            repo = self.github.get_repo(repo_name)
            print(f"repo is {repo}")
            # Get PR
            pr = repo.get_pull(pr_number)
            print(f"pr is {pr}")
            # Get PR details
            pr_data = {
                "title": pr.title,
                "description": pr.body,
                "state": pr.state,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "files_changed": [],
                "commits": []
            }
            
            # Get files changed
            for file in pr.get_files():
                pr_data["files_changed"].append({
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch
                })
            
            # Get commits
            for commit in pr.get_commits():
                pr_data["commits"].append({
                    "sha": commit.sha,
                    "message": commit.commit.message,
                    "author": commit.author.login if commit.author else None,
                    "date": commit.commit.author.date.isoformat()
                })
            
            return pr_data
            
        except GithubException as e:
            print(f"GitHub API error: {e}")
            raise
        except Exception as e:
            print(f"Error fetching PR data: {e}")
            raise

    def get_repo_data(self, repo_name: str) -> Dict[str, Any]:
        """Get repository data."""
        try:
            repo = self.github.get_repo(repo_name)
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "default_branch": repo.default_branch
            }
        except GithubException as e:
            print(f"GitHub API error: {e}")
            raise
        except Exception as e:
            print(f"Error fetching repository data: {e}")
            raise 