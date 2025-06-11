from typing import Dict, Any
from app.models.pr_analysis import PRAnalysis
from app.services.llm_service import (
    get_llm,
    get_pr_analysis_prompt,
    process_llm_output,
    write_raw_output_to_file
)

def analyze_pr(repo: str, pr_number: str) -> Dict[str, Any]:
    """Analyze a pull request using LLM."""
    try:
        # Initialize LLM and prompt
        llm = get_llm()
        prompt = get_pr_analysis_prompt()
        
        # Create chain
        chain = prompt | llm
        
        # Run analysis
        raw_output = chain.invoke({
            "repo": repo,
            "pr_number": pr_number
        })
        
        # Write raw output to file
        output_file = write_raw_output_to_file(raw_output, repo, pr_number)
        print(f"Raw output written to: {output_file}")
        
        # Process output
        processed_output = process_llm_output(raw_output)
        
        # Create Pydantic model
        analysis_result = PRAnalysis(
            summary=processed_output["summary"],
            comments=processed_output["comments"],
            risk_level=processed_output["risk_level"]
        )
        
        return {
            "status": "success",
            "analysis": analysis_result.model_dump(),
            "output_file": output_file
        }
        
    except Exception as e:
        print(f"Error in analyze_pr: {e}")
        return {
            "status": "error",
            "error": str(e),
            "analysis": PRAnalysis(
                summary="Unable to analyze PR",
                comments=["An error occurred during analysis"],
                risk_level="Unknown"
            ).model_dump()
        } 