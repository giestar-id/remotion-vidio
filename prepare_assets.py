import os
import shutil
import json
import docx

def prepare():
    os.makedirs('public/stickman', exist_ok=True)
    
    # 1. Parse docx
    doc = docx.Document('assets/naskah2.docx')
    table = doc.tables[0]
    scenes = []
    for idx, row in enumerate(table.rows[1:], start=1):
        script = row.cells[1].text.strip().replace('\r\n', ' ').replace('\n', ' ')
        visual = row.cells[2].text.strip().replace('\r\n', ' ').replace('\n', ' ') if len(row.cells) > 2 else ''
        anim = row.cells[3].text.strip().replace('\r\n', ' ').replace('\n', ' ') if len(row.cells) > 3 else ''
        scenes.append({
            'id': idx,
            'script': script,
            'visual': visual,
            'animation': anim
        })
    
    with open('public/stickman/scenes.json', 'w', encoding='utf-8') as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)
    print(f'Wrote {len(scenes)} scenes to public/stickman/scenes.json')
    
    # 2. Copy/Link images
    # Map Scene_001.jpg to scene-1.jpg
    for idx in range(1, len(scenes) + 1):
        src_cand1 = f'assets/visual2/Scene_{idx:03d}.jpg'
        src_cand2 = f'assets/visual2/Scene_{idx}.jpg'
        src_cand3 = f'assets/visual2/scene_{idx}.jpg'
        
        src_file = None
        for cand in [src_cand1, src_cand2, src_cand3]:
            if os.path.exists(cand):
                src_file = cand
                break
                
        if src_file:
            dst_file = f'public/stickman/scene-{idx}.jpg'
            if not os.path.exists(dst_file) or os.path.getsize(dst_file) != os.path.getsize(src_file):
                shutil.copy2(src_file, dst_file)
        else:
            print(f'Warning: Image for scene {idx} not found!')
            
    print(f'Images synchronized to public/stickman/scene-<id>.jpg')
    
    # 3. Audio
    audio_src = 'assets/audio2.wav'
    audio_dst = 'public/stickman/voiceover.wav'
    if os.path.exists(audio_src):
        if not os.path.exists(audio_dst) or os.path.getsize(audio_dst) != os.path.getsize(audio_src):
            shutil.copy2(audio_src, audio_dst)
        print('Audio copied to public/stickman/voiceover.wav')
    else:
        print('Error: assets/audio2.wav not found!')

if __name__ == '__main__':
    prepare()

