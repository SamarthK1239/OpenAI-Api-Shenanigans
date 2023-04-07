import moviepy.editor as mp
from pydub import AudioSegment
import os


def get_audio_from_video(path):
    # Load Video File
    clip = mp.VideoFileClip(r"" + path + "\input_video.mp4")
    # Set a base bitrate for the audio (this affects filesize)
    base_bitrate = 65
    # Write the audio track to a mp3
    clip.audio.write_audiofile(r"" + path + "\output_audio.mp3", bitrate=str(base_bitrate) + 'k')
    # Regenerate the audio with a lower bitrate depending on the filesize generated
    audio_compressor(path, clip, base_bitrate)
    print("Conversion Successfully Completed")


def audio_compressor(path, clip, bitrate):
    # Set initial reduction factor of 1.2
    reduction_factor = 1.2
    # Keep redoing the reduction until the filesize <= 25MB
    while check_file_size(path):
        # Find reduced bitrate
        reduced_bitrate = int(bitrate / reduction_factor)
        # Write the audio to the same file, using the new bitrate
        clip.audio.write_audiofile(r"" + path + "\output_audio.mp3", bitrate=str(reduced_bitrate) + 'k')
        # Increase the reduction factor
        reduction_factor += 0.2


# Deprecated method, used to split up the audio as per the input number of minutes
def fetch_first_5_minutes(path, minutes):
    # Load Audio
    audio = AudioSegment.from_mp3(path + "\output_audio.mp3")
    # AudioSegment uses milliseconds, so convert minutes to milliseconds
    millis = minutes * 60 * 1000
    # Extract and write reduced length audio
    reduced_length_audio = audio[:millis]
    reduced_length_audio.export(path + "\output_audio_15.mp3", format="mp3")


# Helper function to determine the file size
def check_file_size(path):
    # Load File
    file = path + "\output_audio.mp3"
    # Load file stats
    stats = os.stat(file)

    # Check if files are > 25mb
    if (stats.st_size / (1024 * 1024)) > 25:
        return True
    else:
        return False


# Currently unused function, intended to simplify the use of these functions
def video_to_audio_handler(path):
    pass


# Driver Code
get_audio_from_video("D:\Random Files")
