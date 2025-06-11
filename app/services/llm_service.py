import json
from datetime import datetime
from typing import Any, Dict
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from app.core.config import LLM_MODEL, LLM_TEMPERATURE, OUTPUT_DIR
from app.models.pr_analysis import PRAnalysis

def write_raw_output_to_file(raw_output: Any, repo: str, pr_number: str) -> str:
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

def process_llm_output(output: Any) -> Dict[str, Any]:
    """Process the LLM output into a structured format."""
    try:
        # If output is a string, try to parse it as JSON
        if isinstance(output, str):
            try:
                # Extract just the JSON part (everything before any additional text)
                json_str = output.split('\n\n')[0]  # Take only the first part before double newline
                # First attempt to parse the outer JSON string
                parsed = json.loads(json_str)
                # If the parsed result is still a string, it might be double-encoded
                if isinstance(parsed, str):
                    try:
                        # Try to parse the inner JSON string
                        parsed = json.loads(parsed)
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse inner JSON string: {e}")
                        return {
                            "summary": "Unable to analyze PR",
                            "comments": ["Invalid JSON response from LLM"],
                            "risk_level": "Unknown"
                        }
                output = parsed
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

def get_pr_analysis_prompt() -> ChatPromptTemplate:
    """Get the PR analysis prompt template."""
    return ChatPromptTemplate.from_messages([
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
        If you have any explanation, add it inside properties.summary.description string.
        
        If you cannot analyze the PR, still use this format but explain why in the summary."""),
        ("user", """Please analyze the following PR:
        Repository: {repo}
        PR Number: {pr_number}
        
        Provide a detailed analysis with:
        1. A summary of the changes
        2. A list of specific comments and suggestions
        3. A risk level assessment (Low/Medium/High)
         
         """)
    ])

def get_llm() -> OllamaLLM:
    """Get the LLM instance."""
    return OllamaLLM(
        model=LLM_MODEL,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        temperature=LLM_TEMPERATURE
    ) 