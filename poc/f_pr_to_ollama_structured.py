import os
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
    try:
        print("starting pr review...\n\n")
        pull_request_details = fetch_pull_request_details(repo, pr_number)
        print(f"pr details are {pull_request_details}\n\n")
        
        print("calling llm to review...\n\n")
        raw_output = call_ollama_with_structure(pull_request_details, PRReview.model_json_schema(), "llama3.2:latest")
        print("Validating json...")
        review = PRReview.model_validate_json(raw_output)
        print(f"\n\nRaw Ollama output: {raw_output}\n\n")
        print(f"review is {review}\n\n")

        for comment in review.code_change_comments:
            if comment.commit_sha and comment.position and comment.path and comment.comment:
                single_comment_on_pr(repo, pr_number, GITHUB_TOKEN, comment.commit_sha, comment.position, comment.path, comment.comment)
        if review.main_comment:
            review_comment_on_pr(repo, pr_number, GITHUB_TOKEN, review.main_comment)
        return review
    except Exception as e:
        print(f"could not comment on PR... {e}")

pr_to_ollama_structured("pr-opper", 5)

print("file ran successfully....")