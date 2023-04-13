import os
from pathlib import Path

from dotenv import load_dotenv
import openai

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Setting organization and API keys
openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")

# Read transcription file
with open("transcription.txt") as f:
    transcription = f.readline()

# Parameter Meanings for response generation
# temperature: Controls Randomness. Lower means less random completions. As this value approaches zero, the model becomes very deterministic
# max_tokens: Maximum of 4000 tokens shared between prompt and completion (input and output)
# top_p: Controls diversity. 0.5 means half of all weighted options are considered
# frequency_penalty: Penalizes new tokens based on frequencies. Decreases the chances of repetition of the same lines
# presence_penalty: Penalizes new tokens based on if they show up already. Increases the likelihood of new topics coming up
# best_of: Generates the specified number of items and then returns the best one

# First generation pass using davinci-003 model
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

# Fact Checking pass, uses same model as above
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

# Detail-addition pass, using same model as above
final_detailed_response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Add as much detail as you can to each bullet point. Split them up into additional bullet points if needed:\n" +
           fact_checked_response["choices"][0]["text"],
    temperature=0.3,
    max_tokens=512,
    top_p=0.5,
    frequency_penalty=0.5,
    presence_penalty=1.4
)

# Print final response after all three passes
print("Final Result", final_detailed_response["choices"][0]["text"])
