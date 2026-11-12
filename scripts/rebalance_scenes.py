import json
import re

def rebalance():
    with open('public/stickman/scenes.json', 'r', encoding='utf-8') as f:
        scenes = json.load(f)

    print(f"Original scenes count: {len(scenes)}")
    
    # We will do a multi-pass or precise split at sentence boundaries.
    # A scene should end at punctuation [.?!] whenever the following words
    # represent the beginning of the next sentence/clause.
    
    # Let's inspect each scene from 0 to N-2
    changes = []
    
    for i in range(len(scenes) - 1):
        curr = scenes[i]
        nxt = scenes[i+1]
        
        script = curr['script'].strip()
        
        # Look for sentence endings followed by words
        # e.g., "blabla. Kata Kata Kata"
        # We find the LAST period, exclamation mark, or question mark in the string that is followed by words
        m = list(re.finditer(r'([.?!])\s+([A-Z0-9\"][^.?!]*)$', script))
        if m:
            match = m[-1]
            punct_pos = match.start(1)
            punct = match.group(1)
            tail = match.group(2).strip()
            
            # Check length of tail in words
            tail_words = tail.split()
            
            # If tail is between 1 and 6 words, it's clearly a stranded start of the next sentence!
            if 1 <= len(tail_words) <= 6:
                clean_curr = script[:punct_pos + 1].strip()
                clean_nxt = tail + ' ' + nxt['script'].strip()
                
                changes.append({
                    'from_id': curr['id'],
                    'to_id': nxt['id'],
                    'moved': tail,
                    'old_curr': script,
                    'new_curr': clean_curr,
                    'new_nxt': clean_nxt
                })
                
                curr['script'] = clean_curr
                nxt['script'] = clean_nxt

    print(f"Applied {len(changes)} sentence-boundary adjustments!")
    
    # Validate: no empty scripts, total word count must be identical
    orig_total_words = sum(len(s['script'].split()) for s in json.load(open('public/stickman/scenes.json', encoding='utf-8')))
    new_total_words = sum(len(s['script'].split()) for s in scenes)
    
    print(f"Original total words: {orig_total_words}")
    print(f"New total words     : {new_total_words}")
    assert orig_total_words == new_total_words, "Word count mismatch!"
    
    for s in scenes:
        assert len(s['script'].strip()) > 0, f"Scene {s['id']} has empty script!"
        
    # Backup original scenes.json
    with open('public/stickman/scenes.json.bak', 'w', encoding='utf-8') as f:
        json.dump(json.load(open('public/stickman/scenes.json', encoding='utf-8')), f, ensure_ascii=False, indent=2)
        
    # Save updated scenes.json
    with open('public/stickman/scenes.json', 'w', encoding='utf-8') as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)
        
    print("Saved public/stickman/scenes.json successfully!")

if __name__ == '__main__':
    rebalance()

