import os
from pathlib import Path

from dotenv import load_dotenv
import openai

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

# Set organization and api keys
openai.organization = os.getenv('organization')
openai.api_key = os.getenv("api_key")


# transcription function
def transcribe(file_path):
    # Open audio file
    audio_file = open(file_path + '\output_audio.mp3', "rb")

    # Use Whisper-1 model to transcribe audio file
    transcription = openai.Audio.transcribe("whisper-1", audio_file)

    # Write output to txt file in root directory
    with open('transcription.txt', 'w') as f:
        f.write(transcription['text'])


# Driver Code
transcribe("D:\Random Files")
