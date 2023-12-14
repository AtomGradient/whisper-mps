# whisper-mps

An opinionated CLI to transcribe Audio files w/ Whisper on-device! Powered by  *MLX*, *Whisper* & *Apple M series*

**TL;DR** - After our actual testing. The Whisper supported by MPS achieves speeds comparable to 4090! 80 mins audio file only need 80s on APPLE M1 MAX 32G! ONLY 80 SECONDS


## 🆕 Blazingly fast transcriptions via your terminal! ⚡️

We've added a CLI to enable fast transcriptions. Here's how you can use it:

Install `whisper-mps` with `pip`:

```bash
pip install whisper-mps
```

Run inference from any path on your computer:

```bash
whisper-mps --file-name < wav filename >
```


> [!NOTE]
> The CLI is highly opinionated and only works on Apple MPS.

## CLI Options

The `whisper-mps` repo provides an all round support for running Whisper in various settings. More command-line support will be provided later

```
  --file-name FILE_NAME
                        Path or URL to the audio file to be transcribed.
```
