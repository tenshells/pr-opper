from typing import override
from pydantic import BaseModel, Field
from datetime import datetime

class PurFiles(BaseModel):
    filename: str = Field(
        title="path of file in repo where code changes occur",
        description="use this string as path in output"
    )
    status: str
    additions: int
    deletions: int
    changes: int
    blob_url: str
    raw_url: str
    contents_url: str
    patch: str = Field(
        title="patch of changes",
        description="actual additions/deletions/changes in each file")

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
    commit_sha: str = Field(
        title="sha hash of commit",
        description="description of commit"
    )
    message: str = Field(
        title="message added to commit",
        description="words about what changes commit is meant to do")
    files: list[PurFiles] = Field(
        description="list of file changes"
    )

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


class PurPullRequestMeta(BaseModel):
    title: str = Field(
        title="title of pull request")
    body: str | None
    state: str
    user: str
    created_at: datetime
    updated_at: datetime | None
    closed_at: datetime | None
    merged_at: datetime | None
    base_ref: str

class PurPullRequest(BaseModel):
    meta: PurPullRequestMeta
    commits: list[PurCommits] = Field(
        description="List of commits in pull request, these have the key code changes and commit sha"
    )

    def __str__(self):
        """
        Provides a user-friendly, verbose summary of the pull request,
        including ordered dates, total commit count, and total files affected.
        """
        # Format dates for better readability
        created_at_str = self.meta.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_at_str = self.meta.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.meta.updated_at else "N/A"
        closed_at_str = self.meta.closed_at.strftime("%Y-%m-%d %H:%M:%S") if self.meta.closed_at else "N/A"
        merged_at_str = self.meta.merged_at.strftime("%Y-%m-%d %H:%M:%S") if self.meta.merged_at else "N/A"

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
            f"Title: {self.meta.title}\n"
            f"Description: {self.meta.body if self.meta.body else 'No description provided.'}\n"
            f"Status: {self.meta.state.capitalize()}\n"
            f"Author: {self.meta.user}\n"
            f"Created On: {created_at_str}\n"
            f"Last Updated: {updated_at_str}\n"
            f"Closed On: {closed_at_str}\n"
            f"Merged On: {merged_at_str}\n"
            f"Base Branch: {self.meta.base_ref}\n"
            f"----------------------------\n"
            f"Summary: This pull request involves {num_commits} commits and a total of {total_files_affected} files affected across all commits.\n"
            f"--- Commits Included ---\n{ordered_commits_string}\n"
            f"----------------------------"
        )
