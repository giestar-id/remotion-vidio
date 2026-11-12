import json
import re

with open('public/stickman/scenes.json', 'r', encoding='utf-8') as f:
    scenes = json.load(f)

# Combine full script to understand the full narrative
full_text = " ".join([s['script'] for s in scenes])

# Print each scene with its visual idea and current script
print(f"Total scenes: {len(scenes)}")

# Let's inspect all 114 scenes visual vs script
with open('scripts/all_scenes_visual_vs_script.txt', 'w', encoding='utf-8') as out:
    for s in scenes:
        m = re.search(r'Visual idea:\s*([^.]+)\.', s['visual'])
        v = m.group(1).strip() if m else s['visual'][:80].strip()
        out.write(f"Scene {s['id']:3d}:\n")
        out.write(f"  Visual : {v}\n")
        out.write(f"  Script : {s['script']}\n\n")

print("Exported scripts/all_scenes_visual_vs_script.txt for full review.")

