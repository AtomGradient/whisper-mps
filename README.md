# whisper-mps

<img src="./whisper-mps.jpeg" alt="image" width="50%" height="auto">

An opinionated CLI to transcribe Audio files(or youtube videos) w/ Whisper on-device! Powered by  *MLX*, *Whisper* & *Apple M series*

**TL;DR** - After our actual testing. The Whisper supported by MPS achieves speeds comparable to 4090! 

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
# filetype should be wav/mp3/mp4 etc
whisper-mps --file-name <filename>
```

Run inference from specfic model size:

```bash
# for example,with base model size, others:["tiny", "base", "small", "medium", "large"]
# Larger models require more loading time
# filetype should be wav/mp3/mp4 etc
whisper-mps --file-name <filename> --model-name base
```

Run inference from YOUTUBE URL on your computer:

```bash
# default download behavior is to fetch the video as a mp3 file to save time
whisper-mps --youtube-url https://www.youtube.com/watch\?v\=jaM02mb6JFM
```

> [!NOTE]
> The CLI is highly opinionated and only works on Apple MPS.

## CLI Options

The `whisper-mps` repo provides an all round support for running Whisper in various settings. More command-line support will be provided later

```
  --file-name FILE_NAME
                  Path or URL to the audio file to be transcribed.
  --model-name MODEL_NAME
                  Size of the OPENAI Whisper model name, like tiny(default),base,small,etc      
  --youtube-url URL_ADDRESS
                  The Youtube play url 
  --output-file-name OUTPUT_FILE_NAME
                  The output file name for the transcribed text JSON
```

## WE ARE HIRING
refer here: https://daxiang.feishu.cn/docx/LluCd7J38o9U5pxN3kdcpSh6nEh