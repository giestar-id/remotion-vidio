import json

with open('public/yunani/captions.json', encoding='utf-8') as f:
    caps = json.load(f)
with open('public/yunani/captions.whisper.json', encoding='utf-8') as f:
    wcaps = json.load(f)
with open('public/yunani/scenes.json', encoding='utf-8') as f:
    scenes = json.load(f)
with open('public/yunani/timeline.json', encoding='utf-8') as f:
    tl = json.load(f)

print('=== LOW-MATCH SCENES (<80%) ===')
for s_tl in tl['scenes']:
    if s_tl['matchRatio'] < 0.8:
        sid = s_tl['id']
        sc = scenes[sid - 1]
        w_slice = [f"{w['text'].strip()}({w['startMs']})" for w in wcaps if s_tl['startMs'] - 1500 <= w['startMs'] <= s_tl['endMs'] + 1500]
        print(f"Scene {sid:3d} ({s_tl['matchRatio']*100:.0f}%) [{s_tl['startMs']}-{s_tl['endMs']}ms]:")
        print("  SCRIPT :", sc['script'])
        print("  WHISPER:", " ".join(w_slice))

# Now let's map every word index in captions.json to its timestamps and print per-scene & per-sentence breakdown
idx = 0
with open('scripts/yunani_word_alignment_detail.txt', 'w', encoding='utf-8') as out:
    for sc in scenes:
        words = sc['script'].split()
        n = len(words)
        chunk = caps[idx:idx+n]
        idx += n
        w_str = " ".join(f"{c['text'].strip()}[{c['startMs']}-{c['endMs']}{'?' if c['confidence'] is None else ''}]" for c in chunk)
        # extract visual idea (strip boilerplate prefix/suffix)
        vis = sc['visual']
        vis = vis.replace('2D gritty, faded ochres, charcoal, muted olive, sun-bleached white. ', '')
        vis = vis.replace(' No photorealism, no readable text, no logos, no watermark.', '')
        out.write(f"ROW {sc['id']:3d} ({chunk[0]['startMs']:6d} - {chunk[-1]['endMs']:6d} ms):\n")
        out.write(f"  VO   : {w_str}\n")
        out.write(f"  IMG#{sc['id']:<3d}: {vis}\n\n")

print(f"\nWrote scripts/yunani_word_alignment_detail.txt (total words mapped: {idx}/{len(caps)})")

