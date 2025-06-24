from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from models.pull_request_details import PullRequestDetails

def call_ollama_with_structure(pull_request_details: PullRequestDetails, 
                               output_json_schema, 
                               model="codellama:latest"):
    prompt = PromptTemplate.from_template(
        """Analyze the following {pull_request_details} and comment on any suggested changes for the commits.. Please maintain the same ShelCommit.sha in the output json"""
    )
    print(f"prompt is : \n{prompt}\n\n")

    # Set up the ChatOllama LLM
    llm = ChatOllama(
        model=model,
        temperature=0.8,
        num_predict=256,
        format=output_json_schema,
    )
    print("composing chain...")
    # Compose the chain
    chain = prompt | llm
    print("invoking chain...")
    # Example usage
    print(f"\n\nactual input to llm is: \n{pull_request_details.model_dump()}\n\n")
    result = chain.invoke({"pull_request_details": f"{pull_request_details.model_dump()}"})
    print("chain invoked successfully")
    return result.content