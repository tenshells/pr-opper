from pydantic import BaseModel
from datetime import datetime

class ShelCommits(BaseModel):
    sha: str
    message: str
    

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