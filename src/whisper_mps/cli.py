from . import whisper
from .utils.ytdownloader import download_and_convert_to_mp3
import argparse
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
import json
import logging


parser = argparse.ArgumentParser(description="Automatic Speech Recognition")
parser.add_argument(
    "--file-name",
    required=False,
    type=str,
    help="Path to the audio file to be transcribed.",
)

parser.add_argument(
    "--model-name",
    required=False,
    default="tiny",
    type=str,
    help="Name of the whisper model size. (default: tiny)",
)

parser.add_argument(
    "--youtube-url",
    required=False,
    default=None,
    type=str,
    help="the address from Youtube,like: https://www.youtube.com/watch?v=jaM02mb6JFM",
)

def worker(file_name,model_name):
    with Progress(
        TextColumn("🤗 [progress.description]"),
        BarColumn(style="yellow1", pulse_style="white"),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[yellow]Transcribing...", total=None)
        text = whisper.transcribe(file_name,model=model_name)
        print(text)
        with open("output.json", "w", encoding="utf8") as fp:
            json.dump(text, fp, ensure_ascii=False)
        print(
            f"Voila!✨ Your file has been transcribed go check it out over here 👉 output.json"
        )

def main():
    args = parser.parse_args()
    file_name = args.file_name
    model_name = args.model_name
    youtube_url = args.youtube_url
    if youtube_url is not None:
        print(f'start downloading audios: {args.youtube_url}')
        audio_path = download_and_convert_to_mp3(youtube_url)
        worker(audio_path,model_name)
    else:
        if file_name is None:
            logging.error(f"local file_name should not be none!")
            return None
        worker(file_name,model_name)    

