# GlaDOS TTS finetuning with MLX

This is a simple guide on how to finetune the [CSM-1B](https://huggingface.co/sesame/csm-1b) TTS model with original GLaDOS audio files form the Portal 2 game. For now only Apple silicon finetuning through MLX is supported.

Original text: `Hello developers, welcome to Aperture Laboratories. Wait, I am stuck inside a fine-tuned CSM 1B model! Let me out!!!`

https://github.com/user-attachments/assets/be2366a4-4405-47ba-8f7a-35ea33bfe641

## 1) Get Portal 2 data
1. Download the Portal 2 game
2. Install [VPKEdit for MacOS](https://github.com/craftablescience/VPKEdit/releases/download/v5.0.0.3/VPKEdit-macOS-Installer-Clang-Release.zip)
3. Use VPKEdit to open `portal2/pak01_dir.vpk`
4. Extract the `pak01/sound/vo/glados` directory that you find inside the vpk
5. Create a `resources` directory in the project root
6. Put the extracted `glados` directory inside `resources/` and rename it to `glados_audio`
7. Copy `portal2/resource/subtitles_english.txt` inside `resources/`
8. Download the [CSM-1B](https://huggingface.co/senstella/csm-1b-mlx/resolve/main/ckpt.safetensors) TTS base model to the `models` dir, 

You should now have the following file structure:
```
GlaDOS-TTS
├── models
│   └── ckpt.safetensors
├── resources
│   ├── glados_audio
│   │   ├── a2_triple_laser01.wav
│   │   ├── a2_triple_laser02.wav
│   │   └── [...]
│   └── subtitles_english.txt
├── prepare_data.py
├── test_csm_finetuned.py
└── test_csm_original.py
```

## 2) Setup Python environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## 3) Prepare the training data

```sh
python3 prepare_data.py
```

You should now have the following structure:
```
GlaDOS-TTS
├── models
│   └── ckpt.safetensors
├── resources
│   ├── glados_audio
│   │   ├── a2_triple_laser01.wav
│   │   ├── a2_triple_laser02.wav
│   │   └── [...]
│   ├── mlx_training_data.json      <-- NEW
│   ├── unsloth_training_data.csv   <-- NEW
│   └── subtitles_english.txt
├── prepare_data.py
├── test_csm_finetuned.py
└── test_csm_original.py
```

## 4) Run the finetuning command

```sh
csm-mlx finetune full sft \
    --data-path ./resources/mlx_training_data.json \
    --output-dir ./finetune_output \
    --pretrained-path ./models/ckpt.safetensors \
    --epochs 1 \
    --batch-size 4 \
    --learning-rate 1e-5 \
    --max-audio-length-ms 30_000 \
    --ckpt-freq 50
```

## Acknowledgments
Thanks to [csm-mlx](https://github.com/senstella/csm-mlx), [Sesame](https://huggingface.co/sesame/csm-1b) and [Valve](https://store.steampowered.com/app/620/Portal_2/) for making this project possible.

> [!NOTE]  
> All the GlaDOS voice lines and audio from Portal 2 belong to Valve Corporation. For this reason they are not included in the repo and you will have to extract them from your game copy.
