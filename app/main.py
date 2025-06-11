from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.worker import analyze_pr_task

app = FastAPI()

class PRRequest(BaseModel):
    repo: str
    pr_number: str

@app.post("/analyze")
async def analyze_pr(request: PRRequest):
    """Analyze a pull request."""
    try:
        # Start Celery task
        task = analyze_pr_task.delay(request.repo, request.pr_number)
        
        return {
            "status": "success",
            "message": "Analysis started",
            "task_id": task.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 