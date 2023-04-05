import os
from pathlib import Path

from dotenv import load_dotenv
import openai

import urllib.request
from PIL import Image

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")

response = openai.Image.create(
    prompt=input("Enter a prompt: "),
    n=1,
    size="1024x1024"
)

image_url = response['data'][0]['url']

urllib.request.urlretrieve(image_url, "result.png")
img = Image.open("result.png")
img.show()
