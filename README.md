# whisper-mps

<img src="./whisper-mps.jpeg" alt="image" width="50%" height="auto">

An opinionated CLI to transcribe Audio files (or YouTube videos) w/ Whisper on-device! Powered by *MLX*, *Whisper* & *Apple M series*

**TL;DR** - After our actual testing, the Whisper supported by MPS achieves speeds comparable to a 4090!

80 mins audio file only need 80s on APPLE M1 MAX 32G! ONLY 80 SECONDS

## 🆕 Blazingly fast transcriptions via your terminal! ⚡️

We've added a CLI to enable fast transcriptions. Here's how you can use it:

Install `whisper-mps` with `pip`:

```bash
# please install ffmpeg first: brew install ffmpeg
pip install whisper-mps
```

Run inference from any path on your computer:

```bash
# filetype should be wav/mp3/mp4 etc.
whisper-mps --file-name <filename>
```

Run inference with a specific model size:

```bash
# for example, using the base model size. Other available models: "tiny", "base", "small", "medium", "large".
# Larger models require more loading time.
# filetype should be wav/mp3/mp4 etc.
whisper-mps --file-name <filename> --model-name base
```

Run inference from a YouTube URL on your computer:

> [!NOTE]
> **Deprecated:** The YouTube URL inference feature is deprecated and may be removed in future releases.  
> Please uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download YouTube videos.

```bash
# whisper-mps --youtube-url https://www.youtube.com/watch\?v\=jaM02mb6JFM
```

> [!NOTE]
> The CLI is highly opinionated and only works on Apple MPS.

## CLI Options

The `whisper-mps` repo provides all-round support for running Whisper in various settings. More command-line support will be provided later.

```
  --file-name FILE_NAME
                  Path or URL to the audio file to be transcribed.
  --model-name MODEL_NAME
                  Size of the OPENAI Whisper model name, like tiny (default), base, small, etc.
  --youtube-url URL_ADDRESS
                  The YouTube video URL. (Deprecated)
  --output-file-name OUTPUT_FILE_NAME
                  The output file name for the transcribed text JSON.
  --log-level LOG_LEVEL
                  Optional. ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
```