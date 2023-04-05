import os
from pathlib import Path

from dotenv import load_dotenv
import openai

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")

audio_file = open("D:\OpenAI-Api-Shenanigans\OpenAI-API\output_audio_15.mp3", "rb")

transcription = openai.Audio.transcribe("whisper-1", audio_file)

with open('transcription.txt', 'w') as f:
    f.write(transcription['text'])
