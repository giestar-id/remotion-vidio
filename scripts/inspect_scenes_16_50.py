import json

with open('scripts/scenes_full_data.json', encoding='utf-8') as f:
    scenes = json.load(f)

for s in scenes[15:50]:
    print(f"[{s['scene_num']:3d}] {s['visual_idea']}")
    print(f"      VO: \"{s['voiceover']}\"")
    print(f"      Label: {s['label']}")
    print()

