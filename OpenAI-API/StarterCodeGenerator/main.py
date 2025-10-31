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
client = OpenAI(
    api_key=os.getenv('api_key')
)



