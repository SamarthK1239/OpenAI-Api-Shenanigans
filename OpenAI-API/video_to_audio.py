import moviepy.editor as mp
from pydub import AudioSegment
import os


def get_audio_from_video(path):
    # Load Video File
    clip = mp.VideoFileClip(r"" + path + "\input_video.mp4")
    # Write the audio track to a mp3
    base_bitrate = 65
    clip.audio.write_audiofile(r"" + path + "\output_audio.mp3", bitrate=str(base_bitrate) + 'k')

    audio_compressor(path, clip, base_bitrate)
    print("Conversion Successfully Completed")


def audio_compressor(path, clip, bitrate):
    reduction_factor = 1
    while check_file_size(path):
        bitrate = int(bitrate / reduction_factor)
        clip.audio.write_audiofile(r"" + path + "\output_audio.mp3", bitrate=str(bitrate) + 'k')
        reduction_factor += 1


def fetch_first_5_minutes(path):
    audio = AudioSegment.from_mp3(path + "\output_audio.mp3")
    ten_minutes = 15 * 60 * 1000
    first_10_minutes = audio[:ten_minutes]
    first_10_minutes.export(path + "\output_audio_15.mp3", format="mp3")


def check_file_size(path):
    file = path + "\output_audio.mp3"
    stats = os.stat(file)

    if (stats.st_size / (1024 * 1024)) > 25:
        return True
    else:
        return False


def video_to_audio_handler(path):
    pass


get_audio_from_video("D:\Random Files")
