import json, os, re

with open('scripts/yunani_scenes_raw.json', encoding='utf-8') as f:
    scenes = json.load(f)

print(f"Total scenes in docx: {len(scenes)}")

# Dump clean readable summary of all 161 rows
with open('scripts/yunani_scenes_summary.txt', 'w', encoding='utf-8') as out:
    for s in scenes:
        out.write(f"Scene {s['scene_num']:>3}: VO  = {s['script']}\n")
        out.write(f"          VIS = {s['visual']}\n")
        out.write(f"          ANI = {s['animation']}\n\n")

# Check missing or empty script
empty_scripts = [s['scene_num'] for s in scenes if not s['script'].strip()]
print("Empty scripts:", empty_scripts)

# Check visual directory files
vis_dir = 'assets/yunani/visual'
all_files = sorted(os.listdir(vis_dir))
scene_nums = set()
non_scene = []
for fn in all_files:
    m = re.match(r'^Scene_(\d+)\.jpg$', fn, re.IGNORECASE)
    if m:
        scene_nums.add(int(m.group(1)))
    else:
        non_scene.append(fn)

missing_nums = [i for i in range(1, 162) if i not in scene_nums]
extra_nums = [i for i in sorted(scene_nums) if i < 1 or i > 161]
print(f"Scene_1..161 coverage: {len(scene_nums)} present, missing={missing_nums}, extra={extra_nums}")
print(f"Non-Scene files ({len(non_scene)}):")
for fn in non_scene:
    print("  -", fn)

