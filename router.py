from fastapi import APIRouter, HTTPException
from models import PRRequest
import uuid
import json
from worker import analyze_pr_task, r

router = APIRouter()

@router.post("/analyze")
async def analyze_pr(pr: PRRequest):
    task_id = str(uuid.uuid4())
    print("submitting task")
    analyze_pr_task.delay(pr.repo, pr.pr_number, pr.token, task_id)
    print("submitted task")
    return {"task_id": task_id}

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    result = r.get(task_id)
    if result:
        return json.loads(result)
    return {"status": "processing"}

def register_routes(app):
    app.include_router(router) 