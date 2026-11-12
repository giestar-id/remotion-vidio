import json

with open('scripts/scenes_full_data.json', encoding='utf-8') as f:
    data = json.load(f)

for s in data[:20]:
    print(f"[{s['scene_num']:2d}] VO: {s['voiceover']}")
    print(f"     IDEA : {s['visual_idea']}")
    print(f"     FOCUS: {s['focus']}")
    print(f"     LABEL: {s['label']}")
    print()

