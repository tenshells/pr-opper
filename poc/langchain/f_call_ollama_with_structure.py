from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate


def call_ollama_with_structure(pull_request_details, 
                               output_json_schema, 
                               model="llama3.2:latest"):
    prompt = PromptTemplate.from_template(
        f"""Analyze the following {pull_request_details} and comment on any suggested changes for the commits.."""
    )
    print(prompt)

    # Set up the ChatOllama LLM
    llm = ChatOllama(
        model=model,
        temperature=0.8,
        num_predict=256,
        format=output_json_schema,
    )

    # Compose the chain
    chain = prompt | llm
    # Example usage
    result = chain.invoke({"pull_request_details": f"{pull_request_details}"})
    return result.content