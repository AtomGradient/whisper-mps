import logging
import os
from pathlib import Path
from typing import Optional
import sys
from moviepy.editor import AudioFileClip
from pytube import YouTube
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# download to mp3
def download_and_convert_to_mp3(url: str,
                                output_path: str = "output",
                                filename: str = "test") -> Optional[str]:
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=False).first()

        if audio_stream is None:
            logging.warning("No audio streams found")
            return None

        Path(output_path).mkdir(parents=True, exist_ok=True)

        mp3_file_path = os.path.join(output_path, filename + ".mp4")
        logging.info(f"Downloading started... {mp3_file_path}")

        downloaded_file_path = audio_stream.download(output_path)

        audio_clip = AudioFileClip(downloaded_file_path)
        audio_clip.write_audiofile(mp3_file_path, codec="libmp3lame", verbose=False, logger=None)
        audio_clip.close()

        if Path(downloaded_file_path).suffix != ".mp3":
            os.remove(downloaded_file_path)

        logging.info(f"Download and conversion successful. File saved at: {mp3_file_path}")
        return str(mp3_file_path)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

# download to mp4
def download_and_convert_to_mp4(url: str,
                                output_path: str = "output",
                                filename: str = "test") -> Optional[str]:
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if video_stream is None:
            logging.warning("No video streams found")
            return None

        Path(output_path).mkdir(parents=True, exist_ok=True)

        mp4_file_path = os.path.join(output_path, filename + ".mp4")
        logging.info(f"Downloading started... {mp4_file_path}")

        downloaded_file_path = video_stream.download(output_path)

        if Path(downloaded_file_path).suffix != ".mp4":
            os.remove(downloaded_file_path)

        os.rename(downloaded_file_path, mp4_file_path)
        logging.info(f"Download and conversion successful. File saved at: {mp4_file_path}")
        return str(mp4_file_path)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
    

# below debug:
# download_and_convert_to_mp4(testDownloadURL)
# testDownloadURL="https://www.youtube.com/watch?v=jaM02mb6JFM"
# newYoutubeAddRess=sys.argv[1]
# logging.info(f"New Youtube download video address: {newYoutubeAddRess}")
# download_and_convert_to_mp4(newYoutubeAddRess)