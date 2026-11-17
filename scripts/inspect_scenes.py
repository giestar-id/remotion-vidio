import json

with open('public/orang-indo-pertama/scenes.json', 'r', encoding='utf-8') as f:
    scenes = json.load(f)

with open('public/orang-indo-pertama/captions.whisper.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print(f"Total scenes: {len(scenes)}")
print(f"Total whisper words: {len(words)}")

for i in range(min(25, len(scenes))):
    sc = scenes[i]
    print(f"--- Scene {sc['id']} ---")
    print(f"Naskah: {sc['script']}")
    # print first 100 chars of visual
    print(f"Visual: {sc['visual'][:120]}...")
