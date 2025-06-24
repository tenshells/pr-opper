from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate


def call_ollama_with_structure(pull_request_details, 
                               output_json_schema, 
                               model="llama3.2:latest"):
    prompt = PromptTemplate.from_template(
        """Analyze the following {pull_request_details} and comment on any suggested changes for the commits.. Please track whole commit SHA """
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
    result = chain.invoke({"pull_request_details": f"{pull_request_details}"})
    print("chain invoked successfully")
    return result.content