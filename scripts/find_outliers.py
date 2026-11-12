import json
import re

with open('public/stickman/scenes.json', 'r', encoding='utf-8') as f:
    scenes = json.load(f)

with open('public/stickman/timeline.json', 'r', encoding='utf-8') as f:
    timeline = json.load(f)

print("Checking for short scenes (< 1800ms) or long scenes (> 5500ms):\n")

short_or_long = []
for i, s in enumerate(timeline['scenes']):
    dur = s['endMs'] - s['startMs']
    sc = scenes[i]
    m = re.search(r'Visual idea:\s*([^.]+)\.', sc['visual'])
    v = m.group(1).strip() if m else sc['visual'][:60].strip()
    
    if dur < 1800 or dur > 5500:
        short_or_long.append({
            'id': s['id'],
            'dur': dur,
            'words': s['words'],
            'script': sc['script'],
            'visual': v
        })

print(f"Total outlier scenes: {len(short_or_long)}")
for o in short_or_long:
    print(f"Scene {o['id']:3d} ({o['dur']}ms | {o['words']} words):")
    print(f"  Script: \"{o['script']}\"")
    print(f"  Visual: {o['visual']}\n")

