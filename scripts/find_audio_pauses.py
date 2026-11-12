import json

with open('public/stickman/captions.whisper.json', 'r', encoding='utf-8') as f:
    caps = json.load(f)

print(f"Total tokens in Whisper: {len(caps)}")

pauses = []
for i in range(len(caps) - 1):
    gap = caps[i+1]['startMs'] - caps[i]['endMs']
    if gap >= 200: # 200ms or more of silence/breath
        pauses.append({
            'index': i,
            'word_before': caps[i]['text'].strip(),
            'word_after': caps[i+1]['text'].strip(),
            'endMs': caps[i]['endMs'],
            'nextStartMs': caps[i+1]['startMs'],
            'gapMs': gap
        })

print(f"Found {len(pauses)} natural pauses (>= 200ms) in narration audio!")
print("Top 15 longest pauses:")
for p in sorted(pauses, key=lambda x: -x['gapMs'])[:15]:
    print(f"  {p['gapMs']}ms pause between \"{p['word_before']}\" ({p['endMs']}ms) and \"{p['word_after']}\" ({p['nextStartMs']}ms)")

