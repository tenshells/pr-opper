from typing import override
from pydantic import BaseModel
from datetime import datetime

class PurFiles(BaseModel):
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    blob_url: str
    raw_url: str
    contents_url: str
    patch: str

    def __str__(self):
        """
        Provides a user-friendly, concise string representation of a file's changes.
        """
        return (
            f"- File: {self.filename}\n"
            f"  Status: {self.status}\n"
            f"  Changes: {self.changes} lines ({self.additions} additions, {self.deletions} deletions)\n"
            f"  View URL: {self.blob_url}"
        )



class PurCommits(BaseModel):
    commit_sha: str
    message: str
    files: list[PurFiles]

    def __str__(self):
        """
        Provides a user-friendly, concise string representation of a commit.
        Includes a summary of files changed within this commit.
        """
        num_files_changed = len(self.files)
        return (
            f"  {self.commit_sha[:5]}\t"
            f"  {self.message}\t\t"
            f"  ({num_files_changed})"
        )


class PurPullRequest(BaseModel):
    title: str
    body: str | None
    state: str
    user: str
    created_at: datetime
    updated_at: datetime | None
    closed_at: datetime | None
    merged_at: datetime | None
    base_ref: str
    commits: list[PurCommits]

    def __str__(self):
        """
        Provides a user-friendly, verbose summary of the pull request,
        including ordered dates, total commit count, and total files affected.
        """
        # Format dates for better readability
        created_at_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_at_str = self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else "N/A"
        closed_at_str = self.closed_at.strftime("%Y-%m-%d %H:%M:%S") if self.closed_at else "N/A"
        merged_at_str = self.merged_at.strftime("%Y-%m-%d %H:%M:%S") if self.merged_at else "N/A"

        # Count total commits and files affected across all commits
        num_commits = len(self.commits)
        total_files_affected = sum(len(commit.files) for commit in self.commits)

        # Build the commits string with proper ordering and detail
        ordered_commits_string = ""
        if self.commits:
            for i, commit in enumerate(self.commits):
                ordered_commits_string += f"\n{i+1}/{num_commits}: \t{str(commit)}"
        else:
            ordered_commits_string = "\nNo commits found for this pull request."

        # Construct the final verbose string
        return (
            f"--- Pull Request Details ---\n"
            f"Title: {self.title}\n"
            f"Description: {self.body if self.body else 'No description provided.'}\n"
            f"Status: {self.state.capitalize()}\n"
            f"Author: {self.user}\n"
            f"Created On: {created_at_str}\n"
            f"Last Updated: {updated_at_str}\n"
            f"Closed On: {closed_at_str}\n"
            f"Merged On: {merged_at_str}\n"
            f"Base Branch: {self.base_ref}\n"
            f"----------------------------\n"
            f"Summary: This pull request involves {num_commits} commits and a total of {total_files_affected} files affected across all commits.\n"
            f"--- Commits Included ---\n{ordered_commits_string}\n"
            f"----------------------------"
        )
