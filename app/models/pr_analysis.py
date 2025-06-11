from pydantic import BaseModel, Field
from typing import List

class PRAnalysis(BaseModel):
    summary: str = Field(description="A brief summary of the PR changes")
    comments: List[str] = Field(description="List of specific comments and suggestions about the code")
    risk_level: str = Field(description="Risk level of the changes (Low/Medium/High)") 