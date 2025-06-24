from typing import override
from pydantic import BaseModel
from datetime import datetime

class ShelFiles(BaseModel):
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
        return f"ShelFiles(filename={self.filename}\n, status={self.status}\n, additions={self.additions}\n, deletions={self.deletions}\n, changes={self.changes}\n, blob_url={self.blob_url}\n, raw_url={self.raw_url}\n, contents_url={self.contents_url}\n, patch={self.patch}\n)"

class ShelCommits(BaseModel):
    sha: str
    message: str
    files: list[ShelFiles]

    def __str__(self):
        files_string = "\n".join([str(file) for file in self.files])
        return f"ShelCommits(sha={self.sha}\n, message={self.message}\n, files={files_string}\n)"
    

class PullRequestDetails(BaseModel):
    title: str
    body: str | None
    state: str
    user: str
    created_at: datetime
    updated_at: datetime | None
    closed_at: datetime | None
    merged_at: datetime | None
    base_ref: str
    commits: list[ShelCommits]

    def __str__(self):
        commits_string = "\n".join([str(commit) for commit in self.commits])
        return f"PullRequestDetails(title={self.title}\n, body={self.body}\n, state={self.state}\t, user={self.user}\t, created_at={self.created_at}\t, updated_at={self.updated_at}\t, closed_at={self.closed_at}\t, merged_at={self.merged_at}\t, base_ref={self.base_ref}\n, commits={commits_string}\n)"
