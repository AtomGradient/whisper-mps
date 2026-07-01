# HuggingFace Safetensors → whisper-mps `.pt` Converter

Converts a HuggingFace Whisper model (`.safetensors`) into the OpenAI-style `.pt` checkpoint format expected by [whisper-mps](https://github.com/explodingcamera/whisper-mps).

---

## Requirements

```bash
pip install torch safetensors
```

---

## Usage

**1. Set the model path**

Open `sftensores-to-dot-pt.py` and update `MODEL_PATH` to point to your `.safetensors` file:

```python
MODEL_PATH = "path/to/your/model.safetensors"
```

For example:
```python
MODEL_PATH = "../models/Whisper-ble/model.safetensors"
```

**2. Run the script**

```bash
python utils/sftensores-to-dot-pt.py
```

**3. Output**

The script prints the detected model dimensions and saves `your-model.pt` in the current directory:

```
Detected dims: {'n_mels': 128, 'n_vocab': 51866, 'n_audio_ctx': 1500, ...}
Saved your-model.pt
```

Move the output file to wherever whisper-mps expects your models:

```bash
mv your-model.pt ../models/
```

---

## What it does

HuggingFace Whisper checkpoints use different key names than the original OpenAI Whisper architecture. This script remaps them:

| HuggingFace key | OpenAI / whisper-mps key |
|---|---|
| `model.encoder.layers.*` | `encoder.blocks.*` |
| `model.encoder.layer_norm.*` | `encoder.ln_post.*` |
| `model.encoder.embed_positions.weight` | `encoder.positional_embedding` |
| `model.decoder.layers.*` | `decoder.blocks.*` |
| `model.decoder.layer_norm.*` | `decoder.ln.*` |
| `model.decoder.embed_positions.weight` | `decoder.positional_embedding` |
| `model.decoder.embed_tokens.weight` | `decoder.token_embedding.weight` |
| `*.self_attn.q/k/v_proj.*` | `*.attn.query/key/value.*` |
| `*.encoder_attn.q/k/v_proj.*` | `*.cross_attn.query/key/value.*` |
| `*.fc1.* / *.fc2.*` | `*.mlp.0.* / *.mlp.2.*` |
| `*.final_layer_norm.*` | `*.mlp_ln.*` |

It also auto-detects model dimensions (layer count, head count, state size) from the checkpoint itself, so it works across different Whisper model sizes without any manual configuration.

---

## Compatibility

Tested with **Whisper v3 variants** (e.g. `openai/whisper-large-v3`, fine-tunes based on it).

> **Note:** `n_mels=128` and `n_text_ctx=448` are hardcoded for Whisper v3. If you're using an older Whisper variant (v1/v2), you may need to change these to `n_mels=80` and `n_text_ctx=448` respectively.

---

## Troubleshooting

**`FileNotFoundError`** — The path in `MODEL_PATH` is wrong. Double-check it points to an existing `.safetensors` file.

**`KeyError: encoder.blocks.0.attn.query.weight`** — The key remapping didn't produce the expected keys. Your model may use a different HF architecture variant. Open an issue with the output of `print(list(hf_sd.keys())[:10])`.

**Unexpected dims** — If the detected `n_heads` looks wrong, the model may not use 64-dim-per-head. Check `n_audio_state` and adjust the `n_heads = n_audio_state // 64` line accordingly.
