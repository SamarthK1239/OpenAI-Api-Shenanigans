import os
from pathlib import Path

from dotenv import load_dotenv
import openai

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")

with open("transcription.txt") as f:
    transcription = f.readline()

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Comprehensively summarize this for a university student. Using bullet points to organize the summary, "
           "Go through every piece of advice provided by the speaker. If you can use technical programming terms, be sure to reference them.\n" + transcription,
    temperature=0.3,
    max_tokens=512,
    top_p=0.5,
    frequency_penalty=0.5,
    presence_penalty=1.4,
    best_of=2
)
print(response["choices"][0]["text"])
fact_checked_response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Fact check and clarify each bullet point:\n" + response["choices"][0]["text"],
    temperature=0.3,
    max_tokens=512,
    top_p=0.5,
    frequency_penalty=0.5,
    presence_penalty=1.4
)
print(fact_checked_response["choices"][0]["text"])
final_detailed_response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Add as much detail as you can to each bullet point. Split them up into additional bullet points if needed:\n" + fact_checked_response["choices"][0]["text"],
    temperature=0.3,
    max_tokens=512,
    top_p=0.5,
    frequency_penalty=0.5,
    presence_penalty=1.4
)

print(final_detailed_response["choices"][0]["text"])
