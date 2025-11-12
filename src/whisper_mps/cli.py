from . import whisper
from .utils.ytdownloader import download_and_convert_to_mp3
import argparse
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
import json
import logging


parser = argparse.ArgumentParser(
    description="whisper-mps: Blazingly fast transcriptions via your terminal! ⚡️\n\n"
                "An opinionated CLI to transcribe Audio files (or YouTube videos) w/ Whisper on-device!\n"
                "Powered by MLX, Whisper & Apple M series.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  # Transcribe an audio file with default settings
  whisper-mps --file-name audio.mp3
  
  # Transcribe with a specific model size
  whisper-mps --file-name audio.wav --model-name base
  
  # Transcribe and save to a custom output file
  whisper-mps --file-name audio.mp3 --output-file-name transcript.json
  
  # Control logging verbosity
  whisper-mps --file-name audio.mp3 --log-level WARNING

Available Models:
  tiny, base, small, medium, large
  (Larger models require more loading time but provide better accuracy)

Supported Audio Formats:
  wav, mp3, mp4, m4a, flac, and more (via ffmpeg)

Note: This CLI is optimized for Apple MPS (Metal Performance Shaders).
"""
)

parser.add_argument(
    "--file-name",
    required=False,
    type=str,
    metavar="FILE",
    help="Path or URL to the audio file to be transcribed. Supports various formats: wav, mp3, mp4, etc.",
)

parser.add_argument(
    "--model-name",
    required=False,
    default="tiny",
    type=str,
    metavar="MODEL",
    help='Size of the OpenAI Whisper model. Options: "tiny" (default), "base", "small", "medium", "large". '
         'Larger models provide better accuracy but take longer to load.',
)

parser.add_argument(
    "--youtube-url",
    required=False,
    default=None,
    type=str,
    metavar="URL",
    help="[DEPRECATED] The YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID). "
         "This feature is deprecated and may be removed in future releases. "
         "Please use yt-dlp to download YouTube videos instead.",
)

parser.add_argument(
    "--output-file-name",
    required=False,
    default="output.json",
    type=str,
    metavar="FILE",
    help="The output file name for the transcribed text JSON (default: output.json). "
         "Will automatically append .json extension if not provided.",
)

parser.add_argument(
    "--log-level",
    required=False,
    default="INFO",
    type=str,
    metavar="LEVEL",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    help='Set the logging level to control output verbosity. '
         'Options: DEBUG (most verbose), INFO (default), WARNING, ERROR, CRITICAL (least verbose).',
)

def worker(file_name,model_name,output_file_name):
    with Progress(
        TextColumn("🤗 [progress.description]"),
        BarColumn(style="yellow1", pulse_style="white"),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[yellow]Transcribing...", total=None)
        text = whisper.transcribe(file_name,model=model_name)
        logging.debug(f"Transcription result: {text}")
        with open(output_file_name, "w", encoding="utf8") as fp:
            json.dump(text, fp, ensure_ascii=False)
        logging.info(
            f"Voila!✨ Your file has been transcribed go check it out over here 👉 {output_file_name}"
        )

def main():
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_name = args.file_name
    model_name = args.model_name
    youtube_url = args.youtube_url
    output_file_name = args.output_file_name
    if not output_file_name.lower().endswith('.json'):
        output_file_name = output_file_name + '.json'
    if youtube_url is not None:
        logging.info(f'start downloading audios: {args.youtube_url}')
        audio_path = download_and_convert_to_mp3(youtube_url)
        worker(audio_path,model_name,output_file_name)
    else:
        if file_name is None:
            logging.error("local file_name should not be none!")
            return None
        worker(file_name,model_name,output_file_name)    

