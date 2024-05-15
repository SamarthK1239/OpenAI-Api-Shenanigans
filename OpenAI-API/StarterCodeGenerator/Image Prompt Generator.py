from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
import base64
import requests

path = Path("/Environment-Variables/.env")
load_dotenv(dotenv_path=path)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def local_image(openai, image_path):
    # Load image
    image_path = image_path

    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('api_key')}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Generate a prompt that you can then use to create frontend code to represent the design "
                                "shown in the picture. This should include descriptions of any major elements, "
                                "including positions, colors and other characteristics."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 700
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())


def remote_image(openai, image_path):
    image_path = image_path

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Generate a prompt that you can then use to create frontend code to represent the design "
                             "shown in the picture. This should include descriptions of any major elements, "
                             "including positions, colors and other characteristics."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_path,
                        },
                    },
                ],
            }
        ],
        max_tokens=700,
    )
