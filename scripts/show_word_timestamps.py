import json

with open('public/stickman/captions.whisper.json', encoding='utf-8') as f:
    caps = json.load(f)

print("Exact word timestamps in the first 40 seconds:\n")
for c in caps[:90]:
    txt = c['text'].strip()
    s = c['startMs']
    e = c['endMs']
    print(f"{s:5d} - {e:5d} ms | {txt}")

