from pydantic import BaseModel, Field
from typing import List, Optional

class CommentOnPR(BaseModel):
    """Represents a comment on a specific code change in a PR."""
    commit_sha: str = Field(
        description="The SHA of the commit where this change was made"
    )
    position: int = Field(
        description="The position in the diff where this comment applies (line number)"
    )
    path: str = Field(
        description="The file path where the change was made"
    )
    comment: str = Field(
        description="The actual review comment about this specific change"
    )
    description: Optional[str] = Field(
        None,
        description="Optional detailed description of the change being commented on"
    )

class PRReview(BaseModel):
    """Represents a complete PR review with both main comments and file-specific comments."""
    code_change_comments: List[CommentOnPR] = Field(
        description="List of detailed comments on specific code changes"
    )
    main_comment: str = Field(
        description="Overall summary comment about the PR"
        )