from ollama import chat
from ollama import ChatResponse


response: ChatResponse = chat(model='llama3.2:latest', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?, answer in 10 words',
  },
])
# or access fields directly from the response object
print(response.message.content)
