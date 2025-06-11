from typing import Dict, Any
from app.models.pr_analysis import PRAnalysis
from app.services.llm_service import (
    get_llm,
    get_pr_analysis_prompt,
    process_llm_output,
    write_raw_output_to_file
)
from app.services.github_service import GitHubService

def analyze_pr(repo: str, pr_number: str) -> Dict[str, Any]:
    """Analyze a pull request using LLM."""
    try:
        print(f"\n[PR Service] Starting analysis for PR #{pr_number} in {repo}")
        
        # Initialize GitHub service
        print("[PR Service] Initializing GitHub service...")
        github_service = GitHubService()
        
        # Get PR data from GitHub
        print(f"[PR Service] Fetching PR data from GitHub...")
        pr_data = github_service.get_pr_data(repo, int(pr_number))
        print(f"[PR Service] Successfully fetched PR data:")
        print(f"  - Title: {pr_data['title']}")
        print(f"  - Files changed: {len(pr_data['files_changed'])}")
        print(f"  - Commits: {len(pr_data['commits'])}")
        
        # Initialize LLM and prompt
        print("[PR Service] Initializing LLM and prompt...")
        llm = get_llm()
        prompt = get_pr_analysis_prompt()
        
        # Create chain
        print("[PR Service] Creating LLM chain...")
        chain = prompt | llm
        
        # Prepare PR data for analysis
        print("[PR Service] Preparing PR context for analysis...")
        pr_context = f"""
        PR Title: {pr_data['title']}
        PR Description: {pr_data['description']}
        
        Files Changed:
        {format_files_changed(pr_data['files_changed'])}
        
        Commits:
        {format_commits(pr_data['commits'])}
        """
        print("[PR Service] PR context prepared successfully")
        
        # Run analysis
        print("[PR Service] Invoking LLM chain for analysis...")
        raw_output = chain.invoke({
            "repo": repo,
            "pr_number": pr_number,
            "pr_context": pr_context
        })
        print("[PR Service] LLM analysis completed")
        
        # Write raw output to file
        print("[PR Service] Writing raw output to file...")
        output_file = write_raw_output_to_file(raw_output, repo, pr_number)
        print(f"[PR Service] Raw output written to: {output_file}")
        
        # Process output
        print("[PR Service] Processing LLM output...")
        processed_output = process_llm_output(raw_output)
        print("[PR Service] Output processed successfully")
        
        # Create Pydantic model
        print("[PR Service] Creating Pydantic model...")
        analysis_result = PRAnalysis(
            summary=processed_output["summary"],
            comments=processed_output["comments"],
            risk_level=processed_output["risk_level"]
        )
        print("[PR Service] Pydantic model created successfully")
        
        print("[PR Service] Analysis completed successfully")
        return {
            "status": "success",
            "analysis": analysis_result.model_dump(),
            "output_file": output_file,
            "pr_data": pr_data
        }
        
    except Exception as e:
        print(f"[PR Service] Error in analyze_pr: {e}")
        return {
            "status": "error",
            "error": str(e),
            "analysis": PRAnalysis(
                summary="Unable to analyze PR",
                comments=["An error occurred during analysis"],
                risk_level="Unknown"
            ).model_dump()
        }

def format_files_changed(files: list) -> str:
    """Format the list of changed files for the prompt."""
    if not files:
        return "No files changed"
    
    formatted = []
    for file in files:
        formatted.append(f"- {file['filename']} ({file['status']})")
        formatted.append(f"  +{file['additions']} -{file['deletions']} changes")
        if file.get('patch'):
            formatted.append(f"  Patch: {file['patch'][:200]}...")  # Limit patch size
    return "\n".join(formatted)

def format_commits(commits: list) -> str:
    """Format the list of commits for the prompt."""
    if not commits:
        return "No commits"
    
    formatted = []
    for commit in commits:
        formatted.append(f"- {commit['sha'][:7]}: {commit['message']}")
        if commit['author']:
            formatted.append(f"  Author: {commit['author']}")
    return "\n".join(formatted) 