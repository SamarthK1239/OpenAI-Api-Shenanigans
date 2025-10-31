import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from openai import OpenAI

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# set up the openai client
client = OpenAI(
    api_key=os.getenv("api_key")
)


def create_variation():
    response = client.images.create_variation(
        image=open("generated_image.jpg", "rb"),
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    response = requests.get(image_url)

    # Save and open image on local machine
    with open("generated_image_revised.jpg", "wb") as f:
        f.write(response.content)