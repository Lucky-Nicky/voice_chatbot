import openai
import os

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key ='sk-L95YXqkGeimdD4gGWJdcxLpuGsB4MoCiVxcgEbZq4UHFHjdP'

result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "python有哪些应用领域？"}
    ]
)
# print(result)
# print(type(result))
print(result["choices"][0]["message"]["content"])
