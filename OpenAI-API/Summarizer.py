import os
from pathlib import Path

from dotenv import load_dotenv
import openai

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")