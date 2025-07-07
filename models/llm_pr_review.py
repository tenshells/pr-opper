from pydantic import BaseModel, Field
from typing import List, Optional

class PRComment(BaseModel):
    """Represents a comment on a specific code change in a PR."""
    commit_sha: str = Field(
        title="COMMIT_SHA",
        description="The commit_sha of the commit for appropriate comment change was made",
        pattern="^[a-f0-9]{40}$",
        examples=["3a1b2c4d5e6f7890abcdef1234567890abcdef12"]
    )
    position: int = Field(
        title="position",
        description="The position in the diff where this comment applies (line number)",
        ge=1
    )
    path: str = Field(
        title="file path",
        description="The file path where the change was made, this can be fetched from the filename in the ShelCommit.ShelFile"
    )
    comment: str = Field(
        description="The actual review comment about this specific change"
    )
    description: Optional[str] = Field(
        None,
        description="Optional detailed description of the change being commented on"
    )

class PurReview(BaseModel):
    """Represents a complete PR review with both main comments and file-specific comments."""
    commit_comments: List[PRComment] = Field(
        description="List of detailed comments on specific code changes"
    )
    review_comment: str = Field(
        description="Overall summary comment about the PR"
        )