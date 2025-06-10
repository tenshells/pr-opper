from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uuid
import json
from worker import analyze_pr_task, r
import uvicorn

app = FastAPI()
print("run it up!")

class PRRequest(BaseModel):
    repo: str
    pr_number: int
    token: str  # GitHub PAT or App token

@app.post("/analyze")
async def analyze_pr(pr: PRRequest):
    task_id = str(uuid.uuid4())
    analyze_pr_task.delay(pr.repo, pr.pr_number, pr.token, task_id)
    return {"task_id": task_id}


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    result = r.get(task_id)
    if result:
        return json.loads(result)
    return {"status": "processing"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


