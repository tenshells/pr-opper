from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

# Define the Pydantic schema for structured response
class Country(BaseModel):
    name: str = Field(description="The country's name", required=True)
    population: int = Field(description="The country's population", required=True)
    languages: list[str] = Field(description="The country's official languages", required=True)

# Create a prompt template
prompt = PromptTemplate.from_template(
    """Provide information about a country in a structured format.

Human: {question}
AI: """
)

# Set up the ChatOllama LLM
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.8,
    num_predict=256,
    format=Country.model_json_schema(),
)

# Compose the chain
chain = prompt | llm

# Example usage
result = chain.invoke({"question": "What is Italy's name, population, and official languages?"})
print("Structured output:", result.content)