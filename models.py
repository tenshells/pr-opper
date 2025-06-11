from pydantic import BaseModel, Field
from typing import List

class PRRequest(BaseModel):
    repo: str
    pr_number: int
    token: str  # GitHub PAT or App token

class PRAnalysis(BaseModel):
    summary: str = Field(description="A brief summary of the PR changes")
    comments: List[str] = Field(description="List of specific comments and suggestions about the code")
    risk_level: str = Field(description="Risk level of the changes (Low/Medium/High)") 