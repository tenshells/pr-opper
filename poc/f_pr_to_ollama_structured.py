import os
from poc.github import review_comment_on_pr
from poc.langchain.f_call_ollama_with_structure import call_ollama_with_structure
from poc.github.f_fetch_pull_request_details import fetch_pull_request_details
from poc.github.f_comment_on_pr import single_comment_on_pr
from poc.github.f_review_comment_on_pr import review_comment_on_pr
from models.llm_pr_review import PRReview
from dotenv import load_dotenv

print("running file..")
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def pr_to_ollama_structured(repo, pr_number):
    print("starting pr review...\n\n")
    repo = "pr-opper"
    pr_number = 2
    pr_details = fetch_pull_request_details(repo, pr_number)
    print(f"pr details are {pr_details}\n\n")
    
    print("calling llm to review...\n\n")
    raw_output = call_ollama_with_structure(pr_details, PRReview.model_json_schema(), "llama3.2:latest")
    review = PRReview.model_validate_json(raw_output)
    print(f"Raw Ollama output: {raw_output}\n\n")
    print(f"review is {review}\n\n")

    for comment in review.code_change_comments:
        single_comment_on_pr(repo, pr_number, GITHUB_TOKEN, comment.commit_sha, comment.position, comment.path, comment.comment)
    if review.main_comment:
        review_comment_on_pr(repo, pr_number, GITHUB_TOKEN, review.main_comment)
    return review

pr_to_ollama_structured("pr-opper", 2)

print("file ran successfully....")