from fastapi import APIRouter
import uuid

router = APIRouter()

@router.post("/analyze")
async def analyze_pr():
    task_id = str(uuid.uuid4())
    return {"task_id": task_id}

@router.get("/status/{task_id}")
async def get_status():
    return {"status": "processing"}

def register_routes(app):
    app.include_router(router)