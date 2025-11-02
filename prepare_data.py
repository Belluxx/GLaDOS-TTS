import os
import json
import string

RESOURCES_DIR = 'resources'
INPUT_FILE = os.path.join(RESOURCES_DIR, 'subtitles_english.txt')
AUDIO_DIR = os.path.join(RESOURCES_DIR, 'glados_audio')
CSV_OUTPUT_FILE = os.path.join(RESOURCES_DIR, 'unsloth_training_data.csv')
JSON_OUTPUT_FILE = os.path.join(RESOURCES_DIR, 'mlx_training_data.json')

WORD_BLACKLIST = ['Caroline:']
MIN_CHAR_COUNT = 25

print("Reading subtitles file...")
with open(INPUT_FILE, 'r', errors='replace') as f:
    printable = set(string.printable)
    lines = f.readlines()
    lines = [
        ''.join(filter(lambda x: x in printable, line))
        for line in lines if line.strip()
    ]

csv_rows = []
json_data = []
filtered_count = 0

for i, line in enumerate(lines):
    if 'glados.' in line:
        key_start = line.find('"') + 1
        key_end = line.find('"', key_start)
        key = line[key_start:key_end]
        key = key.replace('glados.', '')
        
        # Extract the text after GLaDOS:
        text_start = line.find('GLaDOS:') + 7
        text = line[text_start:].strip().strip('"')
        
        # Remove color tag at start
        if text.startswith('<clr:'):
            text_start = text.find('>') + 1
            text = text[text_start:].strip()
        
        text_lower = text.lower()
        
        if len(text) < MIN_CHAR_COUNT:
            filtered_count += 1
            continue
        
        if any(word.lower() in text_lower for word in WORD_BLACKLIST):
            filtered_count += 1
            continue
        
        csv_rows.append((key, text))
        
        turn = [{
            "text": text,
            "audio_path": os.path.join(AUDIO_DIR, key + ".wav"),
            "speaker": 0
        }]
        json_data.append(turn)

with open(CSV_OUTPUT_FILE, 'w', encoding='utf-8') as out:
    for key, text in csv_rows:
        out.write(f'{os.path.join(AUDIO_DIR, key + ".wav")},"{text}"\n')

with open(JSON_OUTPUT_FILE, 'w', encoding='utf-8') as out:
    json.dump(json_data, out, indent=4)

print(f"CSV: {len(csv_rows)} entries saved to {CSV_OUTPUT_FILE}")
print(f"JSON: {len(json_data)} entries saved to {JSON_OUTPUT_FILE}")
print(f"Filtered out: {filtered_count} entries")
