from celery import shared_task
from redis import Redis
from app.core.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB
)
from app.services.pr_service import analyze_pr

# Initialize Redis
redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

@shared_task(name='analyze_pr_task')
def analyze_pr_task(repo: str, pr_number: str, task_id: str) -> dict:
    """Celery task to analyze a PR."""
    print(f"\n[PR Task] Starting PR analysis task for PR #{pr_number} in {repo}")
    print(f"[PR Task] Task ID: {task_id}")
    
    try:
        # Run analysis using PR service
        print("[PR Task] Calling PR service for analysis...")
        result = analyze_pr(repo, pr_number)
        print("[PR Task] PR service analysis completed")
        
        # Store result in Redis
        print("[PR Task] Storing result in Redis...")
        redis_client.set(
            task_id,
            str(result["analysis"]),
            ex=3600  # Expire after 1 hour
        )
        print("[PR Task] Result successfully stored in Redis")
        
        print("[PR Task] Task completed successfully")
        return result
        
    except Exception as e:
        print(f"[PR Task] Error in analyze_pr_task: {e}")
        error_result = {
            "status": "error",
            "error": str(e),
            "analysis": {
                "summary": "Unable to analyze PR",
                "comments": ["An error occurred during analysis"],
                "risk_level": "Unknown"
            }
        }
        
        # Store error in Redis
        print("[PR Task] Storing error result in Redis...")
        redis_client.set(
            task_id,
            str(error_result["analysis"]),
            ex=3600  # Expire after 1 hour
        )
        print("[PR Task] Error result stored in Redis")
        
        print("[PR Task] Task completed with error")
        return error_result 