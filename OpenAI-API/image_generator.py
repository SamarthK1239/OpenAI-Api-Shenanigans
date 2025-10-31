import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI

# Get environment variables
path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Set up openai client
client = OpenAI(
    api_key=os.getenv("api_key")
)


def generate_image():
    # Generates n images of the specified size, based on user-provided prompt
    response = client.images.generate(
        model="dall-e-2",
        prompt=input("Enter a prompt: "),
        n=1,
        size="1024x1024"
    )

    # Retrieve web-URL for image
    image_url = response.data[0].url
    response = requests.get(image_url)

    # Save and open image on local machine
    with open("generated_image.jpg", "wb") as f:
        f.write(response.content)
