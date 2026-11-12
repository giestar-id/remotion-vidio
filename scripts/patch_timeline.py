import json

tl = json.load(open('public/sejarah-1/timeline.json', encoding='utf-8'))
for s in tl['scenes']:
    s.setdefault('image', 'sejarah-1/images/scene-%d.jpg' % s['id'])
json.dump(tl, open('public/sejarah-1/timeline.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('images patched:', len(tl['scenes']))

sc = {s['id']: s for s in json.load(open('public/sejarah-1/scenes.json', encoding='utf-8'))}
for i in [104, 165, 168, 204, 209]:
    print(i, '|', sc[i]['script'])
