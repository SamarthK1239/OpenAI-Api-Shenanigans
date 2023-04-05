import moviepy.editor as mp
import pydub
from pydub import AudioSegment
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import os
from pathlib import Path
from dotenv import load_dotenv

path = Path("Environment-Variables/.env")
load_dotenv(dotenv_path=path)

pydub.AudioSegment.ffmpeg = os.getenv('ffmpeg_path')


def get_audio_from_video():
    # Load Video File
    clip = mp.VideoFileClip(r"sample_video.mp4")
    # Write the audio track to a mp3
    clip.audio.write_audiofile(r"output_audio.mp3")
    print("The audio has been stored in 'output_audio.mp3'")


def reduce_audio_file_size():
    mp3File = "output_audio.mp3"
    wavFile = "source_file.wav"

    # Convert .wav to .mp3
    audio = AudioSegment.from_mp3(mp3File)
    audio.export(wavFile, format="wav")

    data, samplerate = sf.read(wavFile)

    n = len(data)  # the length of the arrays contained in data
    Fs = samplerate  # the sample rate
    # Working with stereo audio, there are two channels in the audio data.
    # Let's retrieve each channel separately:
    ch1 = np.array([data[i][0] for i in range(n)])  # channel 1
    ch2 = np.array([data[i][1] for i in range(n)])  # channel 2

    ch1_Fourier = np.fft.fft(ch1)  # performing Fast Fourier Transform
    abs_ch1_Fourier = np.absolute(ch1_Fourier[:n // 2])  # the spectrum
    eps = 1e-5

    frequenciesToRemove = (1 - eps) * np.sum(abs_ch1_Fourier) < np.cumsum(abs_ch1_Fourier)

    f0 = (len(frequenciesToRemove) - np.sum(frequenciesToRemove)) * (Fs / 2) / (n / 2)

    wavCompressedFile = "audio_compressed.wav"
    # Then we define the down-sampling factor
    D = int(Fs / f0)
    print("Down-sampling factor : {}".format(D))
    new_data = data[::D, :]  # getting the down-sampled data
    # Writing the new data into a wav file
    sf.write(wavCompressedFile, new_data, int(Fs / D), 'PCM_16')


def fetch_first_5_minutes():
    song = AudioSegment.from_mp3("output_audio.mp3")
    ten_minutes = 15 * 60 * 1000
    first_10_minutes = song[:ten_minutes]
    first_10_minutes.export("output_audio_15.mp3", format="mp3")


def get_filepath():
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'output_audio.mp3')
    return filename


fetch_first_5_minutes()
