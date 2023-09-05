import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo-0301',
    messages=[
        {'role': 'user', 'content': "python有哪些应用领域？"}
    ],
    stream=True
)

for chunk in response:
    # print(chunk)
    print(chunk["choices"][0]["delta"].get("content", ""), end="")

