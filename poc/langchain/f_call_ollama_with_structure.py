from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from models.pull_request_details import PurPullRequest

def call_ollama_with_structure(pull_request_details: PurPullRequest, 
                               output_json_schema, 
                               model="codellama:latest"):
    prompt = PromptTemplate.from_template(
        """Analyze  {pull_request_details} and recommend changes that would improve code quality and readability on any of the commits submitted, list blocks of changes for each file wise and make sure to use the entire and correct commit_sha from the input to the output.
        """
    )
    print(f"prompt is : \n{prompt}\n\n")

    # Set up the ChatOllama LLM
    llm = ChatOllama(
        model=model,
        temperature=0.8,
        num_predict=256,
        format=output_json_schema,
    )
    print(f"Going to output in \n\n {output_json_schema}\n\n")
    print("composing chain...")
    # Compose the chain
    chain = prompt | llm
    print("invoking chain...")
    # Example usage
    import json
    import os
    from datetime import datetime
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp in ddMM_hhmmAM/PM format
    timestamp = datetime.now().strftime("%d%m_%I%M%p")
    
    # Write the input to a JSON file with timestamp
    output_file = os.path.join(output_dir, f'llm_input_{timestamp}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        # Use mode="json" to ensure datetime fields are properly serialized
        json.dump(pull_request_details.model_dump(mode="json"), f, indent=2, ensure_ascii=False)
    
    print(f"LLM input written to: {output_file}")
    
    # Convert model to JSON-serializable dict before passing to chain
    pr_details_json = pull_request_details.model_dump(mode="json")
    result = chain.invoke({"pull_request_details": json.dumps(pr_details_json)})
    
    # Save LLM output to file with same timestamp
    output_file = os.path.join(output_dir, f'llm_output_{timestamp}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result.content, f, indent=2, ensure_ascii=False)
    
    print(f"LLM output written to: {output_file}")
    print("chain invoked successfully")
    return result.content