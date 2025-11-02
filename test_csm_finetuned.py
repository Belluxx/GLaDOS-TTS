from mlx_lm.sample_utils import make_sampler
from csm_mlx import CSM, csm_1b, generate

import audiofile
import numpy as np

# Initialize the model
MODEL_PATH = "finetune_output/final_model.safetensors"
csm = CSM(csm_1b())
csm.load_weights(MODEL_PATH, strict=True)

# Generate audio from text
audio = generate(
    csm,
    text="Hello developers, welcome to Aperture Laboratories. Wait, I am stuck inside a fine-tuned CSM 1B model! Let me out!!!",
    speaker=0,
    context=[],
    max_audio_length_ms=12_000,
    sampler=make_sampler(temp=0.8, top_k=50),
)

audiofile.write("./audio_finetuned.wav", np.asarray(audio), 24000)
