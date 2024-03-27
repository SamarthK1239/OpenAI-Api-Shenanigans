# Imports
import json
import random


def read_category(category):
    f = open("starter_prompts.json")
    data = json.load(f)

    random_prompt = data[category][random.randint(0, 4)]

    return random_prompt


def record_storyline(response, source, storyline):
    storyline = {"GPT": [], "User": []}
    storyline[source].append(response)
    return storyline

