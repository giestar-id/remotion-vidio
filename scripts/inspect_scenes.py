import json
import os

def inspect_project(proj, scenes_source, max_scenes=25):
    print("="*80)
    print(f"PROJECT: {proj.upper()}")
    print("="*80)
    
    tl_path = f"public/{proj}/timeline.json"
    with open(tl_path, "r", encoding="utf-8") as f:
        tl = json.load(f)
        
    whisper_file = f"public/{proj}/captions.whisper.json"
    if not os.path.exists(whisper_file):
        whisper_file = f"public/{proj}/captions.json"
    with open(whisper_file, "r", encoding="utf-8") as f:
        whisper = json.load(f)
        
    if isinstance(scenes_source, str):
        with open(scenes_source, "r", encoding="utf-8") as f:
            raw_scenes = json.load(f)
    else:
        raw_scenes = scenes_source
        
    for s_idx in range(min(max_scenes, len(tl["scenes"]))):
        s = tl["scenes"][s_idx]
        sid = s["id"]
        start_ms = s["startMs"]
        end_ms = s["endMs"]
        
        # find matching raw scene
        raw = None
        for r in raw_scenes:
            r_id = str(r.get("id", r.get("scene_num", "")))
            if r_id == str(sid):
                raw = r
                break
        visual = raw.get("visual", raw.get("prompt", "N/A")) if raw else "N/A"
        script = raw.get("script", raw.get("vo", "N/A")) if raw else "N/A"
        
        # words in this scene
        words = []
        for w in whisper:
            ws = w.get("startMs", w.get("start", 0))
            we = w.get("endMs", w.get("end", 0))
            txt = w.get("word", w.get("text", ""))
            if ws >= start_ms - 50 and we <= end_ms + 50:
                words.append(txt)
        spoken_text = " ".join(words)
        
        print(f"Scene {sid} [{start_ms}ms - {end_ms}ms] ({end_ms-start_ms}ms)")
        print(f"  VISUAL: {visual[:130]}...")
        print(f"  SCRIPT: {script}")
        print(f"  SPOKEN: {spoken_text}")
        print("-" * 60)

if __name__ == "__main__":
    import sys
    proj = sys.argv[1] if len(sys.argv) > 1 else "majapahit"
    if proj == "china":
        with open("scripts/parsed_naskah_china.json", "r", encoding="utf-8") as f:
            raw = json.load(f)
        inspect_project("china", raw, 22)
    else:
        inspect_project(proj, f"public/{proj}/scenes.json", 22)
