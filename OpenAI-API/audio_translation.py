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

path = r'C:\Users\samar\Downloads\00176131.mp3'
print(path)

audio_file = open(path, "rb")
translation = client.audio.translations.create(
  model="whisper-1",
  file=audio_file
)
print(translation.text)

audio_file = open(path, "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file
)
print(transcription.text)
