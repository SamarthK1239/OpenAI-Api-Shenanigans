import os
from pathlib import Path
import file_operations as fo
from dotenv import load_dotenv
import openai

# Get environment variables
path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Setting organization and API keys
openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")

# Get category
category = input("What category would you like to generate a story from? ")

# Get a random prompt from the category
prompt = fo.read_category(category)

# Set up the starting GPT prompt

