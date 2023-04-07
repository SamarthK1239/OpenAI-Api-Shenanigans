import os
from pathlib import Path

from dotenv import load_dotenv
import openai

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Setting organization and API keys
openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")

# Generate response using davinci-003
# Parameter meanings are listed in Summarizer.py
response = openai.Completion.create(
    model="text-davinci-003",
    # Prompt is hardcoded, I'm lazy lol
    prompt="What is the sentiment of this text? Respond with one of the following: Positive, Negative, Neutral, and rank it on a scale of 1 - 10 where 1 is heavily negative and 10 is heavily positive. \n" + input("What text would you like to classify? "),
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0
)

# Print the response text
print(response['choices'][0]['text'])
