import json
import re

with open('public/stickman/scenes.json', 'r', encoding='utf-8') as f:
    scenes = json.load(f)

# Copy scenes
cleaned_scenes = [dict(s) for s in scenes]

# List of sentence starters and conjunctions that should never be at the end of a scene
# if there is a period/question mark earlier in the scene
starters_regex = re.compile(
    r'([.?!])\s+('
    r'Saat\b|'
    r'Tapi\b|'
    r'Namun\b|'
    r'Namun,\s*kamu\b|'
    r'Dan\b|'
    r'Dan\s+di\b|'
    r'Di\s+sinilah\b|'
    r'Ketika\b|'
    r'Karena\b|'
    r'Padahal\b|'
    r'Begitu\b|'
    r'Maka\b|'
    r'Jika\b|'
    r'Lalu\b|'
    r'Pada\s+tahun\b|'
    r'Sejak\b|'
    r'Orang\s+lain\b|'
    r'Hasilnya\b|'
    r'Dalam\b|'
    r'Hal\s+yang\b|'
    r'Gampangnya,?\b|'
    r'Tidak\s+ada\b|'
    r'Tetapi\b|'
    r'Ternyata\b|'
    r'Tanpa\b|'
    r'Kesadaran\b|'
    r'Jadi,?\b|'
    r'Yang\s+membuatmu\b|'
    r'Mari\s+kita\b|'
    r'Otakmu\b|'
    r'Salinan\b|'
    r'Ramalan\b|'
    r'Gelombang\b|'
    r'Tulang\b|'
    r'Kamu\s+sudah\b|'
    r'Suaramu\b|'
    r'Apakah\b|'
    r'Mereka\b|'
    r'Holzman\b|'
    r'Rasa\s+cemas\b|'
    r'Para\s+peneliti\b|'
    r'Ini\s+membuktikan\b'
    r').*$',
    re.IGNORECASE
)

changes = []

for i in range(len(cleaned_scenes) - 1):
    curr = cleaned_scenes[i]
    nxt = cleaned_scenes[i+1]
    
    curr_script = curr['script'].strip()
    
    # Check if there is a period followed by a stranded sentence/starter at the end of curr
    # Match pattern: sentence ending [.?!] followed by whitespace and words
    m = re.search(r'([.?!])\s+([A-Z0-9][^.?!]*)$', curr_script)
    if m:
        punct = m.group(1)
        stranded = m.group(2).strip()
        
        # We only move it if stranded is a short phrase (< 5 words) or matches a starter
        words_in_stranded = stranded.split()
        if len(words_in_stranded) <= 4 or starters_regex.search(curr_script):
            # Split curr_script at the punctuation
            idx_split = m.start(1) + 1
            new_curr = curr_script[:idx_split].strip()
            new_nxt = stranded + ' ' + nxt['script'].strip()
            
            changes.append({
                'scene_from': curr['id'],
                'scene_to': nxt['id'],
                'moved': stranded,
                'before_curr': curr_script,
                'after_curr': new_curr,
                'before_nxt': nxt['script'].strip(),
                'after_nxt': new_nxt
            })
            
            curr['script'] = new_curr
            nxt['script'] = new_nxt

print(f"Total perubahan kalimat yang diusulkan: {len(changes)}\n")
for ch in changes[:15]:
    print(f"Scene {ch['scene_from']} -> Scene {ch['scene_to']}:")
    print(f"  Pindahkan: \"{ch['moved']}\"")
    print(f"  Scene {ch['scene_from']} jadi: \"{ch['after_curr']}\"")
    print(f"  Scene {ch['scene_to']} jadi  : \"{ch['after_nxt']}\"")
    print()

