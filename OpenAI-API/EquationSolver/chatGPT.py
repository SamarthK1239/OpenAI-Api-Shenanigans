import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

path = Path("D:\Github Repos\OpenAI-Api-Shenanigans\OpenAI-API\Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Set up OpenAI client
client = OpenAI(
    api_key=os.getenv("api_key")
)

def convertProblemToEquation(orgKey, apiKey):
    # Note: orgKey parameter is deprecated but kept for backward compatibility
    local_client = OpenAI(api_key=apiKey)
    word_problem = input("Enter a word problem: ")
    response = local_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Use the word problem from below to create an equation, using any numerical figures from the question. Respond with only a mathematical equation and no text whatsoever. I do not need any explanatory text accompanying the equation. \n" + word_problem
            }
        ],
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    return response.choices[0].message.content

def extractEquation(response, orgKey, apiKey):
    # Note: orgKey parameter is deprecated but kept for backward compatibility
    local_client = OpenAI(api_key=apiKey)
    result = local_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "From this text, extract an equation which i can put into an equation solver such as symbolab, and respond with only the equation and no accompanying text: \n" + response
            }
        ],
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    return result.choices[0].message.content
