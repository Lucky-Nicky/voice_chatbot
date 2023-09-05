import openai
import flask
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

if __name__ == '__main__':

    print(openai.api_key)

