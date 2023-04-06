import os
from pathlib import Path

from dotenv import load_dotenv
import openai

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")


def transcribe(file_path):
    audio_file = open(file_path + '\output_audio.mp3', "rb")

    transcription = openai.Audio.transcribe("whisper-1", audio_file)

    with open('transcription.txt', 'w') as f:
        f.write(transcription['text'])


transcribe("D:\Random Files")
