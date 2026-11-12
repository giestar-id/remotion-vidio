import os, re, json, wave, shutil
import docx
from PIL import Image

BASE = r'assets/sejarah islam/sejarah-2'
wav_path = os.path.join(BASE, 'audio.wav')
with wave.open(wav_path, 'rb') as w:
    ch, sr, nf = w.getnchannels(), w.getframerate(), w.getnframes()
    dur = nf / sr
print(f"AUDIO: {wav_path} | ch={ch}, sr={sr}, frames={nf}, dur={dur:.2f}s ({int(round(dur*1000))} ms)")

doc = docx.Document(os.path.join(BASE, 'naskah.docx'))
print("--- DOCX PARAGRAPHS ---")
for p in doc.paragraphs:
    if p.text.strip():
        print(" ", p.text.strip())

print(f"DOCX tables: {len(doc.tables)}")
scenes = []
for ti, t in enumerate(doc.tables):
    print(f"  Table {ti}: {len(t.rows)} rows x {len(t.columns)} cols")
    header = [c.text.strip().replace('\n', ' ') for c in t.rows[0].cells]
    print(f"    Header: {header}")
    for i, row in enumerate(t.rows[1:], start=1):
        cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
        if len(cells) >= 3 and any(cells):
            scenes.append({
                'row_idx': len(scenes) + 1,
                'scene_num': cells[0],
                'script': cells[1],
                'visual': cells[2],
                'animation': cells[3] if len(cells) > 3 else '',
            })

print(f"Total rows extracted: {len(scenes)}")
with open('scripts/sejarah2_scenes_raw.json', 'w', encoding='utf-8') as f:
    json.dump(scenes, f, ensure_ascii=False, indent=2)

with open('scripts/sejarah2_scenes_summary.txt', 'w', encoding='utf-8') as out:
    for s in scenes:
        out.write(f"Scene {s['scene_num']:>3} (row {s['row_idx']}): VO  = {s['script']}\n")
        out.write(f"                    VIS = {s['visual']}\n")
        out.write(f"                    ANI = {s['animation']}\n\n")

# Inspect visual directory
vis_dir = os.path.join(BASE, 'visual')
vis_files = sorted(os.listdir(vis_dir))
scene_map = {}
non_scene = []
sizes = {}
for fn in vis_files:
    m = re.match(r'^Scene_(\d+)\.(jpg|jpeg|png|webp)$', fn, re.IGNORECASE)
    if m:
        scene_map[int(m.group(1))] = fn
    else:
        non_scene.append(fn)
    with Image.open(os.path.join(vis_dir, fn)) as im:
        im.verify()
        sizes[im.size] = sizes.get(im.size, 0) + 1

print(f"Visual files: total={len(vis_files)}, Scene_N={len(scene_map)}, non-Scene={len(non_scene)} -> {non_scene[:10]}")
print(f"Image dimensions verified: {sizes}")
missing = [i for i in range(1, len(scenes) + 1) if i not in scene_map]
extra = [i for i in sorted(scene_map) if i < 1 or i > len(scenes)]
print(f"Missing scene numbers (1..{len(scenes)}): {missing}, extra: {extra}")

# Prepare public/sejarah-2 assets
os.makedirs('public/sejarah-2', exist_ok=True)
shutil.copy2(wav_path, 'public/sejarah-2/voiceover.wav')
for idx in range(1, len(scenes) + 1):
    if idx in scene_map:
        shutil.copy2(os.path.join(vis_dir, scene_map[idx]), f'public/sejarah-2/scene-{idx}.jpg')
print("Copied voiceover.wav & scene images to public/sejarah-2/")
