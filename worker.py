from celery import Celery
import redis
import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

app = Celery("worker", broker="redis://localhost:6379/0")

r = redis.Redis(host="localhost", port=6379, db=1)

class PRAnalysis(BaseModel):
    summary: str = Field(description="A brief summary of the PR changes")
    comments: List[str] = Field(description="List of specific comments and suggestions about the code")
    risk_level: str = Field(description="Risk level of the changes (Low/Medium/High)")

@app.task
def analyze_pr_task(repo, pr_number, token, task_id):
    # Initialize LangChain components
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    parser = PydanticOutputParser(pydantic_object=PRAnalysis)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert PR analyzer. Your task is to analyze pull requests and provide detailed feedback.
        Focus on code quality, potential issues, and best practices.
        {format_instructions}"""),
        ("user", """Please analyze the following PR:
        Repository: {repo}
        PR Number: {pr_number}
        
        Provide a detailed analysis following the specified format.""")
    ])
    
    chain = prompt | llm | parser
    
    try:
        # In a real implementation, you would fetch PR details using GitHub API
        # For now, we'll use a mock PR for demonstration
        analysis_result = chain.invoke({
            "repo": repo,
            "pr_number": pr_number,
            "format_instructions": parser.get_format_instructions()
        })
        
        # Convert to dict for Redis storage
        result_dict = analysis_result.dict()
        r.set(task_id, json.dumps(result_dict), ex=3600)
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed"
        }
        r.set(task_id, json.dumps(error_result), ex=3600)