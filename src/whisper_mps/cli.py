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

parser.add_argument(
    "--model-name",
    required=False,
    default="tiny",
    type=str,
    help="Name of the whisper model size. (default: tiny)",
)

def main():
    args = parser.parse_args()
    print(f'with params, file: {args.file_name} , model size: {args.model_name}')
    with Progress(
        TextColumn("🤗 [progress.description]"),
        BarColumn(style="yellow1", pulse_style="white"),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[yellow]Transcribing...", total=None)
        # text = whisper.transcribe(speech_file)["text"] ## only for debug
        text = whisper.transcribe(args.file_name,model=args.model_name)
        print(text)
        with open("output.json", "w", encoding="utf8") as fp:
            json.dump(text, fp, ensure_ascii=False)
        print(
            f"Voila!✨ Your file has been transcribed go check it out over here 👉 output.json"
        )