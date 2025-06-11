import os
from dotenv import load_dotenv

load_dotenv()

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 1))

# Celery Configuration
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# Output Configuration
OUTPUT_DIR = "llm_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# LLM Configuration
LLM_MODEL = "llama3.2"
LLM_TEMPERATURE = 0.1 