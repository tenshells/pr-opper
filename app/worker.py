import os
from celery import Celery
from redis import Redis
from app.core.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    CELERY_BROKER_URL
)
from app.services.pr_service import analyze_pr

# Initialize Redis
redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

# Initialize Celery
celery_app = Celery('pr_analyzer', broker=CELERY_BROKER_URL)

@celery_app.task(name='analyze_pr_task')
def analyze_pr_task(repo: str, pr_number: str) -> dict:
    """Celery task to analyze a PR."""
    try:
        # Run analysis
        result = analyze_pr(repo, pr_number)
        
        # Store result in Redis
        redis_client.set(
            f"pr_analysis:{repo}:{pr_number}",
            str(result["analysis"])
        )
        
        return result
        
    except Exception as e:
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
        redis_client.set(
            f"pr_analysis:{repo}:{pr_number}",
            str(error_result["analysis"])
        )
        
        return error_result 