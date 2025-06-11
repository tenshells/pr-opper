from celery import Celery
import redis
import json
import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Union, Any, Dict
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from datetime import datetime

load_dotenv()

celery_app = Celery('pr_analyzer', broker='redis://localhost:6379/0')

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Import tasks to ensure they are registered
celery_app.autodiscover_tasks(['app.tasks'])

r = redis.Redis(host="localhost", port=6379, db=1)

# Create output directory if it doesn't exist
OUTPUT_DIR = "llm_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_raw_output_to_file(raw_output: Any, repo: str, pr_number: str):
    """Write the raw LLM output to a timestamped file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/llm_output_{repo}_{pr_number}_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Raw LLM Output\n")
        f.write(f"==============\n\n")
        f.write(f"Repository: {repo}\n")
        f.write(f"PR Number: {pr_number}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Output:\n")
        f.write(f"-------\n")
        f.write(json.dumps(raw_output, indent=2))
    
    return filename

class PRAnalysis(BaseModel):
    summary: str = Field(description="A brief summary of the PR changes")
    comments: List[str] = Field(description="List of specific comments and suggestions about the code")
    risk_level: str = Field(description="Risk level of the changes (Low/Medium/High)")

def process_llm_output(output: Any) -> Dict[str, Any]:
    """Process the LLM output into a structured format."""
    try:
        # If output is a string, try to parse it as JSON
        if isinstance(output, str):
            try:
                output = json.loads(output)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON string: {e}")
                return {
                    "summary": "Unable to analyze PR",
                    "comments": ["Invalid JSON response from LLM"],
                    "risk_level": "Unknown"
                }

        if "properties" in output:
            props = output["properties"]
            return {
                "summary": props.get("summary", {}).get("description", ""),
                "comments": props.get("comments", []),
                "risk_level": props.get("risk_level", {}).get("description", "Medium")
            }
        return output
    except Exception as e:
        print(f"Error processing output: {e}")
        return {
            "summary": "Unable to analyze PR",
            "comments": ["No PR data available for analysis"],
            "risk_level": "Unknown"
        }

@celery_app.task
def analyze_pr_task(repo, pr_number, token, task_id):
    print("starting celery job")
    llm = OllamaLLM(
        model="llama3.2",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        temperature=0.1
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert PR analyzer. Your task is to analyze pull requests and provide detailed feedback.
        Focus on code quality, potential issues, and best practices.
        
        IMPORTANT: You MUST respond in the following JSON format:
        {{
            "properties": {{
                "summary": {{
                    "description": "Your summary here",
                    "type": "string"
                }},
                "comments": ["Comment 1", "Comment 2"],
                "risk_level": {{
                    "description": "Low/Medium/High",
                    "type": "string"
                }}
            }}
        }}
        
        If you cannot analyze the PR, still use this format but explain why in the summary."""),
        ("user", """Please analyze the following PR:
        Repository: {repo}
        PR Number: {pr_number}
        
        Provide a detailed analysis with:
        1. A summary of the changes
        2. A list of specific comments and suggestions
        3. A risk level assessment (Low/Medium/High)""")
    ])
    
    chain = prompt | llm
    print("chain initialized")
    
    try:
        raw_result = chain.invoke({
            "repo": repo,
            "pr_number": pr_number
        })
        print("chain invoked")
        
        # Write raw output to file before parsing
        output_file = write_raw_output_to_file(raw_result, repo, pr_number)
        print(f"Raw LLM output written to file: {output_file}")
        
        # Process the raw result and create PRAnalysis instance
        processed_output = process_llm_output(raw_result)
        analysis_result = PRAnalysis(**processed_output)
        
        # Store in Redis
        r.set(task_id, json.dumps(analysis_result.model_dump()), ex=3600)
        print("result set in redis")
    except Exception as e:
        print(f"error in try block: {e}")
        error_result = PRAnalysis(
            summary="Error analyzing PR",
            comments=[str(e)],
            risk_level="Unknown"
        )
        r.set(task_id, json.dumps(error_result.dict()), ex=3600)
        print("error result set in redis")
    finally:
        print("celery job completed")