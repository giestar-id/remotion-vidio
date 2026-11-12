import json
import re

def optimize():
    # Load original naskah2 docx raw text to ensure 100% fidelity
    with open('public/stickman/scenes.json.bak', 'r', encoding='utf-8') as f:
        orig_scenes = json.load(f)
        
    with open('public/stickman/captions.whisper.json', 'r', encoding='utf-8') as f:
        whisper_caps = json.load(f)
        
    # We have 114 scenes. Let's make sure that each scene has a balanced script
    # where cuts happen ONLY at natural pauses (breath >= 180ms or punctuation [.?,])
    
    # Let's inspect the word timestamps in whisper
    # Each word in whisper has startMs and endMs
    
    # We want:
    # 1. Start of a new sentence MUST start on the new scene (no trailing "Saat", "Tapi", "Namun", "Pada tahun", etc. on previous scene)
    # 2. If moving a sentence start leaves a scene with < 3 words (< 1.8s), we balance it with a natural clause comma or breath pause.
    
    scenes = [dict(s) for s in orig_scenes]
    
    # Let's define the ideal clean splits for the entire text
    # First, let's collect all words across all scenes
    all_words = []
    for s in scenes:
        all_words.extend(s['script'].split())
        
    print(f"Total words: {len(all_words)}")
    
    # Strategy:
    # For every scene i (0 to 113):
    # - Ensure it doesn't end with a stranded sentence start (e.g. '. Saat', '. Tapi', '. Namun', '. Dan di', '. Pada tahun', '. Sejak', etc.)
    # - If moving that starter would leave scene i with < 4 words, check if the previous scene can spare words or if the cut can happen at a comma.
    
    # Let's run a smart balancer
    for pass_num in range(3):
        for i in range(len(scenes) - 1):
            curr = scenes[i]
            nxt = scenes[i+1]
            
            curr_words = curr['script'].split()
            nxt_words = nxt['script'].split()
            
            # Check for trailing sentence starters
            curr_text = " ".join(curr_words)
            m = re.search(r'([.?!])\s+([A-Z0-9\"][^.?!]*)$', curr_text)
            if m:
                tail = m.group(2).strip()
                tail_words = tail.split()
                # If tail is 1 to 5 words, move it to next scene UNLESS it leaves curr with < 3 words
                if len(curr_words) - len(tail_words) >= 3:
                    # Safe to move!
                    curr['script'] = curr_text[:m.start(1) + 1].strip()
                    nxt['script'] = tail + " " + " ".join(nxt_words)
                    continue
                    
            # Check if next scene starts with a stray punctuation or continuation of a clause that is too short
            # e.g., if curr has 14 words and ends without punctuation, but has a comma in the middle,
            # we can split at the comma to balance lengths!
            if len(curr_words) >= 12 and len(nxt_words) <= 4:
                # Find a comma in curr_words after index 5
                comma_indices = [idx for idx, w in enumerate(curr_words) if w.endswith(',') and idx >= 4 and idx <= len(curr_words) - 3]
                if comma_indices:
                    split_idx = comma_indices[-1] + 1
                    left_part = curr_words[:split_idx]
                    right_part = curr_words[split_idx:]
                    curr['script'] = " ".join(left_part)
                    nxt['script'] = " ".join(right_part) + " " + " ".join(nxt_words)
                    
    # Verification
    total_words_after = sum(len(s['script'].split()) for s in scenes)
    print(f"Total words after balancing: {total_words_after}")
    assert total_words_after == len(all_words), "Word count mismatch!"
    
    for s in scenes:
        w_count = len(s['script'].split())
        assert w_count > 0, f"Scene {s['id']} is empty!"
        
    with open('public/stickman/scenes.json', 'w', encoding='utf-8') as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)
        
    print("Saved optimized public/stickman/scenes.json!")

if __name__ == '__main__':
    optimize()

