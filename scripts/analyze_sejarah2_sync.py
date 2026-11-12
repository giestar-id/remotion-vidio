import json

with open('public/sejarah-2/captions.json', encoding='utf-8') as f:
    caps = json.load(f)
with open('public/sejarah-2/captions.whisper.json', encoding='utf-8') as f:
    wcaps = json.load(f)
with open('public/sejarah-2/scenes.json', encoding='utf-8') as f:
    scenes = json.load(f)
with open('public/sejarah-2/timeline.json', encoding='utf-8') as f:
    tl = json.load(f)

print('=== LOW-MATCH SCENES (<70%) ===')
for s_tl in tl['scenes']:
    if s_tl['matchRatio'] < 0.70:
        sid = s_tl['id']
        sc = scenes[sid - 1]
        w_slice = [f"{w['text'].strip()}({w['startMs']})" for w in wcaps if s_tl['startMs'] - 1500 <= w['startMs'] <= s_tl['endMs'] + 1500]
        print(f"Scene {sid:3d} ({s_tl['matchRatio']*100:.0f}%) [{s_tl['startMs']}-{s_tl['endMs']}ms]:")
        print("  SCRIPT :", sc['script'])
        print("  WHISPER:", " ".join(w_slice))

bad_durs = [c for c in caps if (c['endMs'] - c['startMs'] <= 15) or (c['endMs'] - c['startMs'] > 2200)]
print(f"\nSuspicious caption token durations (<=15ms or >2200ms): {len(bad_durs)}")
for c in bad_durs[:20]:
    print(" ", c)

idx = 0
with open('scripts/sejarah2_word_alignment_detail.txt', 'w', encoding='utf-8') as out:
    for sc in scenes:
        words = sc['script'].split()
        n = len(words)
        chunk = caps[idx:idx+n]
        idx += n
        w_str = " ".join(f"{c['text'].strip()}[{c['startMs']}-{c['endMs']}{'?' if c['confidence'] is None else ''}]" for c in chunk)
        vis = sc['visual']
        for prefix in ['2D illustrated style, ', '2D woodcut style, ']:
            pass
        out.write(f"ROW {sc['id']:3d} ({chunk[0]['startMs']:6d} - {chunk[-1]['endMs']:6d} ms):\n")
        out.write(f"  VO   : {w_str}\n")
        out.write(f"  IMG#{sc['id']:<3d}: {vis}\n\n")

print(f"Wrote scripts/sejarah2_word_alignment_detail.txt (total words mapped: {idx}/{len(caps)})")
