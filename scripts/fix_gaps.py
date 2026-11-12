import json

tl = json.load(open('public/sejarah-1/timeline.json', encoding='utf-8'))
scenes = tl['scenes']
MIN_DUR = 1800   # ms; adegan lebih pendek dari ini dianggap 'kilat'
MIN_PREV = 2000  # ms; adegan sebelumnya tidak boleh jadi terlalu pendek
n_adj = 0

for i in range(len(scenes) - 1, 0, -1):
    cur = scenes[i]
    prev = scenes[i - 1]
    dur = cur['endMs'] - cur['startMs']
    pdur = prev['endMs'] - prev['startMs']
    if dur < MIN_DUR and pdur > MIN_PREV + 400:
        need = MIN_DUR - dur
        prev['endMs'] -= need
        if prev['id'] != 1:
            prev['endMs'] = max(prev['endMs'], prev['startMs'] + MIN_PREV)
        cur['startMs'] = prev['endMs']
        dur = cur['endMs'] - cur['startMs']
        if dur >= MIN_DUR:
            n_adj += 1
            print('Scene %3d: start %d -> %d (dur sekarang %d ms)' % (cur['id'], prev['endMs'] + need, prev['endMs'], dur))

json.dump(tl, open('public/sejarah-1/timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
short = [(s['id'], s['endMs'] - s['startMs']) for s in scenes if s['endMs'] - s['startMs'] < MIN_DUR]
print('disesuaikan:', n_adj, 'sisa pendek:', short)
