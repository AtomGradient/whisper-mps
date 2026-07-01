# import torch
# from safetensors.torch import load_file

# # Load the safetensors file
# state_dict = load_file("../models/""address-to-asr-model""/your-model.safetensors")

# # Save as .pt
# torch.save(state_dict, "your-model.pt")


import torch
from safetensors.torch import load_file


MODEL_PATH = "path/to/your/model.safetensors"

try:
    hf_sd = load_file(MODEL_PATH)
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}")
    print("Please update MODEL_PATH to point to your .safetensors file")
    exit(1)

def remap_keys(hf_sd):
    new_sd = {}
    for k, v in hf_sd.items():
        # strip leading "model."
        k = k.removeprefix("model.")

        # encoder
        k = k.replace("encoder.layers.", "encoder.blocks.")
        k = k.replace("encoder.layer_norm.", "encoder.ln_post.")
        k = k.replace("encoder.embed_positions.weight", "encoder.positional_embedding")

        # decoder
        k = k.replace("decoder.layers.", "decoder.blocks.")
        k = k.replace("decoder.layer_norm.", "decoder.ln.")
        k = k.replace("decoder.embed_positions.weight", "decoder.positional_embedding")
        k = k.replace("decoder.embed_tokens.weight", "decoder.token_embedding.weight")

        # attention projections (encoder self-attn)
        k = k.replace(".self_attn.q_proj.", ".attn.query.")
        k = k.replace(".self_attn.k_proj.", ".attn.key.")
        k = k.replace(".self_attn.v_proj.", ".attn.value.")
        k = k.replace(".self_attn.out_proj.", ".attn.out.")
        k = k.replace(".self_attn_layer_norm.", ".attn_ln.")

        # attention projections (decoder cross-attn)
        k = k.replace(".encoder_attn.q_proj.", ".cross_attn.query.")
        k = k.replace(".encoder_attn.k_proj.", ".cross_attn.key.")
        k = k.replace(".encoder_attn.v_proj.", ".cross_attn.value.")
        k = k.replace(".encoder_attn.out_proj.", ".cross_attn.out.")
        k = k.replace(".encoder_attn_layer_norm.", ".cross_attn_ln.")

        # MLP
        k = k.replace(".fc1.", ".mlp.0.")
        k = k.replace(".fc2.", ".mlp.2.")
        k = k.replace(".final_layer_norm.", ".mlp_ln.")

        new_sd[k] = v
    return new_sd

remapped = remap_keys(hf_sd)

# Detect dims from encoder layer count
n_encoder_layers = max(
    int(k.split("encoder.blocks.")[1].split(".")[0])
    for k in remapped if "encoder.blocks." in k
) + 1
n_decoder_layers = max(
    int(k.split("decoder.blocks.")[1].split(".")[0])
    for k in remapped if "decoder.blocks." in k
) + 1

# medium model (32 encoder layers detected from your error)
n_audio_state = remapped["encoder.blocks.0.attn.query.weight"].shape[0]
n_heads = n_audio_state // 64

dims = {
    "n_mels": 128,
    "n_vocab": remapped["decoder.token_embedding.weight"].shape[0],
    "n_audio_ctx": 1500,
    "n_audio_state": n_audio_state,
    "n_audio_head": n_heads,
    "n_audio_layer": n_encoder_layers,
    "n_text_ctx": 448,
    "n_text_state": n_audio_state,
    "n_text_head": n_heads,
    "n_text_layer": n_decoder_layers,
}

print("Detected dims:", dims)

checkpoint = {
    "dims": dims,
    "model_state_dict": remapped,
}

torch.save(checkpoint, "your-model.pt")
print("Saved your-model.pt")