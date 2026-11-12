import json

with open('scripts/scenes_full_data.json', encoding='utf-8') as f:
    scenes = json.load(f)

# Let's inspect the entire script and map every image to its true visual content
print("Analyzing all 114 visual descriptions...")
with open('scripts/visual_analysis_full.txt', 'w', encoding='utf-8') as f:
    for s in scenes:
        f.write(f"IMAGE #{s['scene_num']:3d}:\n")
        f.write(f"  Visual Idea: {s['visual_idea']}\n")
        f.write(f"  Focus      : {s['focus']}\n")
        f.write(f"  Label      : {s['label']}\n")
        f.write(f"  Original VO: {s['voiceover']}\n\n")

print("Exported scripts/visual_analysis_full.txt")

