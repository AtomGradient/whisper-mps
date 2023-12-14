from . import whisper
import argparse
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
import json

parser = argparse.ArgumentParser(description="Automatic Speech Recognition")
parser.add_argument(
    "--file-name",
    required=True,
    type=str,
    help="Path to the audio file to be transcribed.",
)

def main():
    args = parser.parse_args()
    print('Default with small size model')
    # text = whisper.transcribe(speech_file)["text"] ## only for debug
    text = whisper.transcribe(args.file_name)
    print(text)
    with open("output.json", "w", encoding="utf8") as fp:
        json.dump(text, fp, ensure_ascii=False)
    print(
        f"Voila!✨ Your file has been transcribed go check it out over here 👉 output.json"
    )