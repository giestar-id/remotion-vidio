import json
import re

with open('public/stickman/scenes.json', 'r', encoding='utf-8') as f:
    scenes = json.load(f)

with open('public/stickman/timeline.json', 'r', encoding='utf-8') as f:
    timeline = json.load(f)

with open('public/stickman/captions.json', 'r', encoding='utf-8') as f:
    captions = json.load(f)

print('=== ANALISIS STRUKTUR KALIMAT & PERGANTIAN GAMBAR ===\n')

word_idx = 0
scene_data = []

for i, sc in enumerate(scenes):
    tl = timeline['scenes'][i]
    words = sc['script'].split()
    sc_caps = captions[word_idx:word_idx + len(words)]
    word_idx += len(words)
    
    scene_data.append({
        'id': sc['id'],
        'script': sc['script'],
        'words': words,
        'caps': sc_caps,
        'visual': sc['visual'],
        'startMs': tl['startMs'],
        'endMs': tl['endMs']
    })

# Check sentence boundaries vs scene boundaries
orphan_issues = []
for i in range(len(scene_data) - 1):
    curr = scene_data[i]
    nxt = scene_data[i+1]
    
    curr_script = curr['script']
    # Check if there is a period in curr_script that is not at the end
    # e.g., "mesin perunggu yang berputar. Saat"
    period_match = re.search(r'([.?!])\s+([A-Z][a-zA-Z0-9,-]*(\s+[a-zA-Z0-9,-]+){0,3})\s*$', curr_script)
    if period_match:
        orphan = period_match.group(2)
        orphan_issues.append({
            'scene': curr['id'],
            'next_scene': nxt['id'],
            'orphan_text': orphan,
            'full_curr': curr_script,
            'next_start': nxt['words'][:3]
        })

print(f"Total scene dengan 'kalimat baru terpotong di akhir scene': {len(orphan_issues)}")
for item in orphan_issues:
    print(f"\n[Scene {item['scene']} -> {item['next_scene']}]")
    print(f"  Teks Scene {item['scene']} : \"{item['full_curr']}\"")
    print(f"  Kata nyangkut di akhir : \"{item['orphan_text']}\"")
    print(f"  Lanjutan di Scene {item['next_scene']} : \"{' '.join(item['next_start'])} ...\"")

