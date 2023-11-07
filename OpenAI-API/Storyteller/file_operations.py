# Imports
import json
import random


def read_category(category):
    f = open("starter_prompts.json")
    data = json.load(f)

    random_prompt = data[category][random.randint(0, len(data[category]))]

    return random_prompt


def record_storyline(response, source):
    f = open("storyline.json")
    data = json.load(f)

    data[source] = response

    with open("storyline.json", "w") as outfile:
        json.dump(data, outfile)
