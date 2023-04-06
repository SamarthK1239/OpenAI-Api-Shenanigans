import moviepy.editor as mp
from pydub import AudioSegment
import os
from pathlib import Path
from dotenv import load_dotenv

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)


def get_audio_from_video():
    # Load Video File
    clip = mp.VideoFileClip(r"D:\Random Files\sample_video.mp4")
    # Write the audio track to a mp3
    clip.audio.write_audiofile(r"D:\Random Files\output_audio.mp3")
    print("The audio has been stored in 'output_audio.mp3'")


def fetch_first_5_minutes():
    song = AudioSegment.from_mp3("D:\Random Files\output_audio.mp3")
    ten_minutes = 15 * 60 * 1000
    first_10_minutes = song[:ten_minutes]
    first_10_minutes.export("D:\Random Files\output_audio_15.mp3", format="mp3")


def get_filepath():
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'output_audio.mp3')
    return filename


fetch_first_5_minutes()
