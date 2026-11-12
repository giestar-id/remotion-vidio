import os
import re
import shutil
import json

src_dir = 'assets/visual2-2'
dest_dir = 'public/stickman2'
os.makedirs(dest_dir, exist_ok=True)

files = os.listdir(src_dir)
pattern = re.compile(r'^Scene_(\d+)_(.+)\.jpg$', re.IGNORECASE)

mapping = {}
for f in files:
    m = pattern.match(f)
    if m:
        mapping[int(m.group(1))] = f

print(f'Found {len(mapping)} scenes in {src_dir}')

# Copy all 114 images as scene-1.jpg .. scene-114.jpg
for num in range(1, 115):
    src_file = os.path.join(src_dir, mapping[num])
    dest_file = os.path.join(dest_dir, f'scene-{num}.jpg')
    shutil.copy2(src_file, dest_file)

print('All 114 scene images copied to public/stickman2/')

# Copy voiceover.wav, captions.json, captions.whisper.json, scenes.json
for f in ['voiceover.wav', 'captions.json', 'captions.whisper.json', 'scenes.json']:
    src_path = os.path.join('public/stickman', f)
    dest_path = os.path.join(dest_dir, f)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f'Copied {f}')

# Load timeline.json and create stickman2 timeline
with open('public/stickman/timeline.json', encoding='utf-8') as f:
    tl = json.load(f)

tl2 = {
    'audioDurationMs': tl['audioDurationMs'],
    'audio': 'stickman2/voiceover.wav',
    'scenes': []
}

for s in tl['scenes']:
    scene_id = s['id']
    tl2['scenes'].append({
        'id': scene_id,
        'startMs': s['startMs'],
        'endMs': s['endMs'],
        'image': f'stickman2/scene-{scene_id}.jpg'
    })

with open(os.path.join(dest_dir, 'timeline.json'), 'w', encoding='utf-8') as f:
    json.dump(tl2, f, indent=2)

print('public/stickman2/timeline.json generated successfully!')

