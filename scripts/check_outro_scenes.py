import json

with open('scripts/scenes_full_data.json', encoding='utf-8') as f:
    scenes = json.load(f)

for s in scenes[104:]:
    print(f"Scene {s['scene_num']}:")
    print(f"  Idea : {s['visual_idea']}")
    print(f"  Prompt: {s['full_prompt'][:160]}...")
    print(f"  VO   : {s['voiceover']}\n")

