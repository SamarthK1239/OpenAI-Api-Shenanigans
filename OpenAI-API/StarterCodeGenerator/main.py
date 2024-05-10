# Take an image describing a task, ask GPT-4 Vision to evaluate what design elements are, and ask it to generate
# starter code for it. If it is pseudocode, ask gpt-4 to create sample code for it.
# Intention is to help kickstart the coding process and/or start off the process of building a frontend
# Integrate the batch API down the line if results aren't needed immediately

from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
import base64
import requests

path = Path("/Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Initialize openai object
openai = OpenAI(
    organization=os.getenv('organization'),
    api_key=os.getenv('api_key')
)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Load image
image_path = ""

base64_image = encode_image(image_path)
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('api_key')}"
}

payload = {
    "model": "gpt-4-turbo",
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
