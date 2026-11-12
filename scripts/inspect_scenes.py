import json
import re

with open('public/stickman/scenes.json', 'r', encoding='utf-8') as f:
    scenes = json.load(f)

for i in range(9, 23):
    sc = scenes[i]
    m = re.search(r'Visual idea:\s*([^.]+)\.', sc['visual'])
    v = m.group(1) if m else sc['visual'][:60]
    print(f"Scene {sc['id']}:")
    print(f"  Script: \"{sc['script']}\"")
    print(f"  Visual: {v}\n")

