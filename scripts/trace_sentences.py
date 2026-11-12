import json

with open('scripts/scenes_full_data.json', encoding='utf-8') as f:
    scenes_full = json.load(f)
    
with open('public/stickman/captions.whisper.json', encoding='utf-8') as f:
    whisper_caps = json.load(f)

# Find words and their timestamps
words = []
for c in whisper_caps:
    t = c['text'].strip()
    if t:
        words.append({'text': t, 'startMs': c['startMs'], 'endMs': c['endMs']})

print(f"Total whisper words: {len(words)}")

# Let's inspect sentences and their start/end timestamps from 53s to 120s
for i in range(120, 260):
    w = words[i]
    if '.' in w['text'] or '?' in w['text'] or ',' in w['text']:
        print(f"{w['startMs']:5d} - {w['endMs']:5d} ms | {w['text']}")

