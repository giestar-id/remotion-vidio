import json

with open('public/stickman/captions.whisper.json', encoding='utf-8') as f:
    caps = json.load(f)

# Group whisper tokens into sentences
sentences = []
curr = []
for c in caps:
    curr.append(c)
    txt = c['text'].strip()
    if txt.endswith('.') or txt.endswith('?') or txt.endswith('!'):
        s_text = " ".join([x['text'].strip() for x in curr])
        sentences.append({
            'startMs': curr[0]['startMs'],
            'endMs': curr[-1]['endMs'],
            'text': s_text,
            'words': len(curr)
        })
        curr = []

if curr:
    s_text = " ".join([x['text'].strip() for x in curr])
    sentences.append({
        'startMs': curr[0]['startMs'],
        'endMs': curr[-1]['endMs'],
        'text': s_text,
        'words': len(curr)
    })

print(f"Total full sentences: {len(sentences)}")
with open('scripts/all_sentences_with_timing.txt', 'w', encoding='utf-8') as f:
    for idx, s in enumerate(sentences, 1):
        f.write(f"Sentence {idx:3d} ({s['startMs']:6d} - {s['endMs']:6d} ms | {((s['endMs']-s['startMs'])/1000):.2f}s):\n")
        f.write(f"  \"{s['text']}\"\n\n")

print("Exported scripts/all_sentences_with_timing.txt")

