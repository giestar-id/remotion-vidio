import docx, json, re, io

d = docx.Document('assets/sejarah-1/naskah.docx')
t = d.tables[0]
tl = json.load(open('public/sejarah-1/timeline.json', encoding='utf-8'))
tim = {s['id']: s for s in tl['scenes']}

out = io.StringIO()
for r in t.rows[1:]:
    num = int(r.cells[0].text.strip())
    script = ' '.join(r.cells[1].text.split()).strip()
    img = ' '.join(r.cells[2].text.split()).strip()
    m = re.search(r'\[([^\]]+)\]', img)
    subj = m.group(1) if m else img[:42]
    tm = tim[num]
    out.write('%03d | %6.1fs | %-40s | %s\n' % (num, tm['startMs']/1000, subj[:40], script))

with open('scripts/review_gap.txt', 'w', encoding='utf-8') as f:
    f.write(out.getvalue())
print('written')
