from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel

class Country(BaseModel):
  name: str
  population: int
  languages: list[str]

response: ChatResponse = chat(model='llama3.2:latest', messages=[
  {
    'role': 'user',
    'content': 'Tell me about Italy'
  }],
  format=Country.model_json_schema(),
)
# or access fields directly from the response object

country = Country.model_validate_json(response.message.content)

print(country)
