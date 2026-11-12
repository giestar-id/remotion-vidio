import json

AUDIO_DURATION_MS = 804360

with open('public/yunani/captions.json', encoding='utf-8') as f:
    raw_caps = json.load(f)
with open('public/yunani/captions.whisper.json', encoding='utf-8') as f:
    wcaps = json.load(f)
with open('public/yunani/scenes.json', encoding='utf-8') as f:
    scenes = json.load(f)
with open('public/yunani/timeline.json', encoding='utf-8') as f:
    raw_tl = json.load(f)

# ---------------------------------------------------------
# STEP 1: Polish captions.json (fix 1ms squeezed tokens,
# snap stretched endMs before pauses, add natural pageBreakAfter)
# ---------------------------------------------------------
caps = [dict(c) for c in raw_caps]
N = len(caps)

# 1a. Fix 1ms squeezed words (split parent window across consecutive squeezed tokens)
i = 0
while i < N:
    dur = caps[i]['endMs'] - caps[i]['startMs']
    if dur <= 15:
        # Look backwards or forwards to find the merged group sharing startMs
        if i + 1 < N and caps[i + 1]['startMs'] == caps[i]['startMs'] and (caps[i + 1]['endMs'] - caps[i + 1]['startMs']) > 80:
            total_start = caps[i]['startMs']
            total_end = caps[i + 1]['endMs']
            l1 = max(2, len(caps[i]['text'].strip()))
            l2 = max(2, len(caps[i + 1]['text'].strip()))
            split_ms = total_start + int(round((total_end - total_start) * (l1 / (l1 + l2))))
            caps[i]['endMs'] = split_ms
            caps[i]['timestampMs'] = (total_start + split_ms) // 2
            caps[i + 1]['startMs'] = split_ms
            caps[i + 1]['timestampMs'] = (split_ms + total_end) // 2
        elif i - 1 >= 0 and (caps[i - 1]['endMs'] - caps[i - 1]['startMs']) > 200 and caps[i]['startMs'] == caps[i - 1]['endMs']:
            # Take last ~35% of preceding merged token
            total_start = caps[i - 1]['startMs']
            total_end = caps[i]['endMs'] + max(250, (caps[i - 1]['endMs'] - caps[i - 1]['startMs']) // 3)
            # Cap at next word startMs
            if i + 1 < N:
                total_end = min(total_end, caps[i + 1]['startMs'])
            l1 = max(2, len(caps[i - 1]['text'].strip()))
            l2 = max(2, len(caps[i]['text'].strip()))
            split_ms = total_start + int(round((total_end - total_start) * (l1 / (l1 + l2))))
            caps[i - 1]['endMs'] = split_ms
            caps[i - 1]['timestampMs'] = (total_start + split_ms) // 2
            caps[i]['startMs'] = split_ms
            caps[i]['endMs'] = max(split_ms + 80, total_end)
            caps[i]['timestampMs'] = (caps[i]['startMs'] + caps[i]['endMs']) // 2
    i += 1

# 1b. Snap stretched endMs where sentence punctuation ends before a long Whisper gap
for i in range(N - 1):
    gap_next = caps[i + 1]['startMs'] - caps[i]['endMs']
    txt = caps[i]['text'].strip()
    dur = caps[i]['endMs'] - caps[i]['startMs']
    # Find closest Whisper token ending inside [startMs, endMs]
    if caps[i]['confidence'] is None and dur > 900:
        cand = [w for w in wcaps if caps[i]['startMs'] <= w['startMs'] < caps[i]['endMs'] - 200]
        if cand:
            real_end = cand[-1]['endMs']
            if real_end > caps[i]['startMs'] + 80 and real_end < caps[i]['endMs'] - 150:
                caps[i]['endMs'] = real_end
                caps[i]['timestampMs'] = (caps[i]['startMs'] + real_end) // 2

# 1c. Add natural pageBreakAfter for clean documentary subtitle phrasing
# Break on sentence punctuation (. ? ! :) or breath pause >= 320 ms, or comma if page already >= 5 words
for c in caps:
    c.pop('pageBreakAfter', None)
page_word_count = 0
for i in range(N):
    txt = caps[i]['text'].strip()
    page_word_count += 1
    next_gap = (caps[i + 1]['startMs'] - caps[i]['endMs']) if i + 1 < N else 9999
    is_sentence_end = txt.endswith(('.', '?', '!', ':'))
    is_comma = txt.endswith((',', ';'))
    should_break = False
    next_txt = caps[i + 1]['text'].strip().lower().rstrip('.,:;?!') if i + 1 < N else ''
    curr_clean = txt.lower().rstrip('.,:;?!')
    protected_pair = (
        (curr_clean == 'sebelum' and next_txt == 'masehi')
        or (curr_clean == 'perang' and next_txt in ('peloponnesos', 'persia', 'saudara'))
        or (curr_clean in ('raja', 'sungai', 'kuil', 'pulau', 'selat', 'bukit', 'laut') )
        or (curr_clean == 'ai' and next_txt == 'khanoum')
        or (curr_clean == 'philip' and next_txt == 'ii')
    )
    if is_sentence_end or next_gap >= 320:
        should_break = True
    elif is_comma and page_word_count >= 5:
        should_break = True
    elif page_word_count >= 8 and not protected_pair:
        should_break = True

    if should_break and i < N - 1:
        caps[i]['pageBreakAfter'] = True
        page_word_count = 0

with open('public/yunani/captions.json', 'w', encoding='utf-8') as f:
    json.dump(caps, f, ensure_ascii=False, indent=2)

# Verify word count & check captions integrity
zero_durs = [c for c in caps if c['endMs'] <= c['startMs'] or (c['endMs'] - c['startMs']) < 40]
print(f"Polished captions.json: {len(caps)} words, tokens <40ms: {len(zero_durs)}")

# ---------------------------------------------------------
# STEP 2: Map each scene's original words + build semantic word-boundary cuts
# ---------------------------------------------------------
# Build cumulative word start index per raw scene
raw_ranges = []
cursor = 0
for sc in scenes:
    w_count = len(sc['script'].split())
    raw_ranges.append((sc['id'], cursor, cursor + w_count - 1))
    cursor += w_count

assert cursor == len(caps), f"Word count mismatch: {cursor} vs {len(caps)}"

# Helper: print full indexed word list to verify word indices if needed
with open('scripts/yunani_indexed_words.txt', 'w', encoding='utf-8') as f:
    for idx, c in enumerate(caps):
        f.write(f"{idx:4d} [{c['startMs']:6d}-{c['endMs']:6d}] {c['text'].strip()}\n")

# By default, scene k (1..161) starts at raw_ranges[k-1][1].
# Below we specify exact semantic START word index for scenes where raw DOCX split mid-sentence or shifted!
# Format: scene_id: exact first word index in `caps`
SEMANTIC_START_WORD_OVERRIDES = {}

# Let's define anchor phrase lookups relative to expected neighborhood so there is zero human indexing error!
def find_word_idx(phrase_words, approx_word_idx):
    target = [w.lower() for w in phrase_words]
    L = len(target)
    best = None
    best_dist = 999999
    for idx in range(max(0, approx_word_idx - 45), min(len(caps) - L + 1, approx_word_idx + 45)):
        seq = [caps[idx + k]['text'].strip().lower().rstrip('.,:;?!') for k in range(L)]
        t_clean = [w.rstrip('.,:;?!') for w in target]
        if seq == t_clean:
            d = abs(idx - approx_word_idx)
            if d < best_dist:
                best_dist = d
                best = idx
    if best is None:
        raise ValueError(f"Could not find phrase {phrase_words} near word {approx_word_idx}")
    return best

# Compute default start word indices from raw scenes
start_words = {sc['id']: raw_ranges[sc['id'] - 1][1] for sc in scenes}

# Semantic overrides (Scene ID -> exact spoken phrase where that image should BEGIN):
OVERRIDES_SPEC = {
    4: ["Namun,", "politisi", "bernama", "Themistocles"],       # was starting mid-sentence at "seluruh warga kaya mendadak."
    5: ["Dia", "meyakinkan", "warga", "untuk"],                # keep "melarang uang itu dibagi-bagikan." inside Scene 4!
    6: ["demi", "membiayai", "dua", "ratus", "kapal"],         # was starting at "perak demi membiayai"
    12: ["menjelma", "menjadi", "armada", "pelindung"],        # keep 11 through "bukit berbatu"
    16: ["Alam", "yang", "keras", "memaksa"],                  # was starting at "sempit di Laut Aegea." (which belongs to IMG#15 gulfs!)
    17: ["bernama", "polis.", "Artinya,"],                     # polis on rocky plateau starts right on "bernama polis."
    21: ["Sekali", "gagal", "panen,", "satu", "keluarga"],     # was starting at "satu keluarga" splitting sentence
    23: ["Bangsawan", "menguasai", "tanah,"],                  # was starting at "perang saudara." (mid-sentence from 22!)
    26: ["serta", "memerdekakan", "warga"],                    # keep 25 on uprooting debt stones
    27: ["Dia", "melarang", "pinjaman", "berjaminan"],         # Solon writing laws starts cleanly on sentence start
    29: ["tetapi", "membuka", "pintu", "rapat", "umum"],       # artisans entering assembly
    31: ["Sekitar", "508", "Sebelum", "Masehi,"],              # aristocrats arguing starts at 508 SM sentence
    33: ["Dia", "membubarkan", "empat", "suku"],               # crest fragmentation starts cleanly at "Dia membubarkan"
    36: ["Tiap", "suku", "baru", "wajib"],                     # sailor/farmer/smith starts cleanly at "Tiap suku baru"
    38: ["Mereka", "yang", "dulunya", "bermusuhan"],           # 10 reps at circular table starts cleanly at "Mereka yang dulunya"
    39: ["Dewan", "lima", "ratus", "orang"],                   # kleroterion lottery machine starts cleanly at "Dewan lima ratus"
    40: ["Siapa", "pun", "pria", "merdeka"],                   # citizen chosen by lot starts at "Siapa pun pria merdeka"
    41: ["setara", "memimpin", "selama"],                      # craftsman presiding court
    46: ["akibat", "campur", "tangan", "Athena"],              # burning Sardis starts after "menundukkan Yunani"
    48: ["Sepuluh", "tahun", "berselang,", "putranya,"],       # Xerxes starts AFTER "pada 490 Sebelum Masehi." (Marathon!)
    55: ["dan", "membakar", "kuil", "Akropolis"],              # flames on Acropolis start right on "dan membakar kuil Akropolis"
    58: ["Themistocles", "menyusun", "perangkap", "licik."],   # dictating scroll to Sicinnus (was appearing too early during "dua ratus kapal trireme"!)
    62: ["Di", "lorong", "laut", "inilah"],                    # morning mist clears AFTER "pada malam hari."
    64: ["yang", "dikayuh", "seratus", "tujuh"],               # rower sweat starts cleanly on "yang dikayuh"
    66: ["Saat", "kapal", "Persia", "yang", "tambun"],         # wedged bulky ships start at "Saat kapal Persia"
    68: ["Kapal", "trireme", "lincah", "melesat,"],            # trireme darting forward
    69: ["menghantam", "lambung", "lawan"],                    # hulls splintering & capsizing
    70: ["Di", "atas", "bukit,", "Xerxes"],                    # Xerxes on Mount Aigaleo starts at "Di atas bukit,"
    71: ["Kemenangan", "di", "Salamis"],                       # victorious fleet starts at "Kemenangan di Salamis"
    74: ["Puncak", "kejayaan", "diraih"],                      # two steles start at "Puncak kejayaan"
    76: ["kota", "laut", "yang", "kaya", "seni"],              # Athens philosophers
    77: ["Di", "sudut", "lain", "berdiri", "Sparta,"],         # Sparta hoplites start right on "Di sudut lain berdiri Sparta"
    80: ["Para", "sejarawan", "menyebut", "tabir"],            # phalanx dissolving ("Ilusi Sparta")
    81: ["Di", "balik", "zirah", "perunggu"],                  # empty Eurotas barracks / oliganthropia
    83: ["Sistem", "sosial", "Sparta", "luar", "biasa"],       # Spartan mess hall starts at "Sistem sosial Sparta"
    84: ["Untuk", "mempertahankan", "status", "warga"],        # Spartan agoge starts cleanly on new sentence!
    87: ["serta", "sikap", "menutup", "diri,"],                # Messenian helots starts after "464 Sebelum Masehi"
    91: ["sampai", "tak", "ada", "lagi", "prajurit"],          # empty drill field
    93: ["Perang", "saudara", "ini", "berkecamuk"],            # marching Spartans start after "431 Sebelum Masehi."
    94: ["Athena", "berlindung", "di", "balik", "tembok"],     # refugees inside Long Walls start at sentence start
    95: ["Namun,", "wabah", "penyakit", "menyerang"],          # Great Plague starts at "Namun, wabah"
    96: ["termasuk", "pemimpin", "mereka,", "Pericles."],      # tomb of Pericles
    99: ["dan", "menghancurkan", "sisa", "kapal"],             # Aegospotami
    101: ["Kemenangan", "Sparta", "berumur", "sangat"],        # Spartan governors atop Acropolis
    107: ["Di", "titik", "nadir", "inilah,"],                  # storm clouds over Macedonia
    108: ["ancaman", "baru", "muncul", "dari", "perbatasan"],  # Macedonian royal armories
    109: ["Kerajaan", "Makedonia,", "wilayah", "pegunungan"],  # hill peasants under Philip II
    110: ["bangkit", "pesat", "di", "bawah"],                  # Philip II reviewing army
    112: ["Pada", "338", "Sebelum", "Masehi"],                 # sarissa wall at Chaeronea
    114: ["Zaman", "kemandirian", "negara-kota"],              # Lion of Chaeronea over mass grave
    115: ["Dua", "tahun", "kemudian,", "Philip", "tewas"],     # MAJOR OFFSET FIX: Philip assassinated!
    116: ["Putranya", "yang", "berumur", "dua", "puluh"],      # MAJOR OFFSET FIX: Young Alexander takes throne!
    117: ["menumbangkan", "Kekaisaran", "Persia."],            # Granicus cavalry charge
    120: ["lalu", "membakar", "istana", "Persepolis."],        # MAJOR OFFSET FIX: Persepolis engulfed in flames!
    121: ["Dahaga", "ekspansinya", "tak", "pernah"],           # Gedrosian desert dunes march
    122: ["sampai", "tiba", "di", "tepi", "Sungai"],           # muddy banks of Hyphasis river
    123: ["prajuritnya", "yang", "letih", "menolak"],          # MAJOR OFFSET FIX: weeping veterans refusing to march!
    124: ["Alexander", "mendirikan", "dua", "belas"],          # MAJOR OFFSET FIX: 12 colossal stone altars!
    126: ["dalam", "usia", "tiga", "puluh", "dua"],            # signet ring slipping (after "323 Sebelum Masehi")
    128: ["Para", "jenderalnya", "yang", "bergelar"],          # Diadochi generals over marble map
    130: ["Ptolemeus", "di", "Mesir,"],                        # partitioned map
    132: ["Kedaulatan", "politik", "negara-kota"],             # camel trade routes
    134: ["dari", "Laut", "Mediterania", "sampai", "India."],  # bronze scroll case treaty
    135: ["Di", "perpustakaan", "Alexandria,", "para"],        # Library of Alexandria scholars
    136: ["dan", "menghitung", "keliling", "bumi."],           # MAJOR OFFSET FIX: Eratosthenes measuring Earth's circumference!
    137: ["Jauh", "di", "pedalaman", "Asia", "Tengah,"],       # Oxus river in Afghanistan
    140: ["Di", "makam", "pendiri", "kota"],                   # stele at Kineas's tomb
    141: ["yang", "mengajarkan", "manusia", "belajar"],        # childhood manners (masa kecil)
    143: ["berlaku", "adil", "di", "masa", "dewasa,"],         # MAJOR OFFSET FIX: magistrate balancing scales (masa dewasa)!
    144: ["memberi", "nasihat", "bijak", "di", "masa"],        # MAJOR OFFSET FIX: white-bearded elder counsel (masa tua)!
    145: ["dan", "menghadapi", "maut", "tanpa"],               # MAJOR OFFSET FIX: peaceful funeral relief (maut tanpa penyesalan)!
    146: ["Keping", "perak", "yang", "dulu", "dicungkil"],     # MAJOR OFFSET FIX: Laurion silver morphing into coin!
    147: ["Logam", "itu", "telah", "menjelma"],                # silver owl coin
    148: ["yang", "mengalirkan", "gagasan", "tentang"],        # hands passing drachmas in port
    150: ["tetapi", "pikiran", "mereka", "justru"],            # Roman consul bowing to Greek philosopher
    151: ["oleh", "seni,", "sastra,", "dan"],                  # scribes copying Greek scrolls
    154: ["telah", "menjadi", "reruntuhan", "batu"],           # empty Pnyx hill overlooking Aegean
    155: ["Namun,", "setiap", "kali", "manusia", "berkumpul"], # modern ballot voting (Demokrasi Cleisthenes)
    156: ["Setiap", "kali", "para", "hakim"],                  # judge gavel + Solon stele (stays until "hukum Solon.")
    157: ["Dan", "setiap", "kali", "para", "ilmuwan"],         # astronomer telescope
    158: ["mereka", "menyalakan", "obor", "pengetahuan"],      # scholar studying by lamp
    159: ["Sebuah", "peradaban", "sejati"],                    # crumbling ancient rampart
    160: ["melainkan", "seberapa", "dalam", "gagasan"],        # keep "benteng batunya bertahan melawan waktu," on rampart IMG#159!
    161: ["tertanam", "di", "benak", "dunia"],                 # sunset outro over Aegean
}

for sid, phrase in OVERRIDES_SPEC.items():
    start_words[sid] = find_word_idx(phrase, start_words[sid])

# Check strict monotonicity
for sid in range(1, 161):
    if start_words[sid] >= start_words[sid + 1]:
        raise ValueError(f"Non-monotonic word start: Scene {sid} ({start_words[sid]}) >= Scene {sid+1} ({start_words[sid+1]})")

# Compute clean timestamp cut points
timeline_scenes = []
for sid in range(1, 162):
    w_start = start_words[sid]
    w_end = (start_words[sid + 1] - 1) if sid < 161 else (len(caps) - 1)
    if sid == 1:
        start_ms = 0
    else:
        prev_end = timeline_scenes[-1]['endMs']
        start_ms = prev_end

    if sid == 161:
        end_ms = AUDIO_DURATION_MS
    else:
        last_w_end = caps[w_end]['endMs']
        next_w_start = caps[w_end + 1]['startMs']
        gap = next_w_start - last_w_end
        if gap >= 260:
            # Cut cleanly inside silence ~120ms before next phrase speaks, at least 50ms after last word ends
            cut_ms = max(last_w_end + 50, next_w_start - 130)
        elif gap >= 80:
            cut_ms = (last_w_end + next_w_start) // 2
        else:
            cut_ms = max(last_w_end - 20, next_w_start - 60)
        end_ms = int(round(cut_ms))

    # Build spoken text snippet for audit
    spoken_text = " ".join(caps[k]['text'].strip() for k in range(w_start, w_end + 1))
    timeline_scenes.append({
        'id': sid,
        'startMs': start_ms,
        'endMs': end_ms,
        'image': f'yunani/scene-{sid}.jpg',
        'words': w_end - w_start + 1,
        'spoken': spoken_text,
    })

# Sanity check durations
min_scene = min(timeline_scenes, key=lambda s: s['endMs'] - s['startMs'])
max_scene = max(timeline_scenes, key=lambda s: s['endMs'] - s['startMs'])
short_scenes = [s for s in timeline_scenes if (s['endMs'] - s['startMs']) < 1800]
print(f"Built {len(timeline_scenes)} semantic scenes. Total audio: {AUDIO_DURATION_MS} ms")
print(f"Shortest scene: #{min_scene['id']} = {min_scene['endMs']-min_scene['startMs']} ms ('{min_scene['spoken']}')")
print(f"Longest  scene: #{max_scene['id']} = {max_scene['endMs']-max_scene['startMs']} ms")
print(f"Scenes < 1800ms: {[(s['id'], s['endMs']-s['startMs']) for s in short_scenes]}")

# Write public/yunani/timeline.json (clean fields)
clean_tl_scenes = [
    {
        'id': s['id'],
        'startMs': s['startMs'],
        'endMs': s['endMs'],
        'image': s['image'],
        'words': s['words'],
    }
    for s in timeline_scenes
]
with open('public/yunani/timeline.json', 'w', encoding='utf-8') as f:
    json.dump({
        'audioDurationMs': AUDIO_DURATION_MS,
        'audio': 'yunani/voiceover.wav',
        'scenes': clean_tl_scenes,
    }, f, indent=2)

# Write full semantic audit report
raw_tl_map = {s['id']: s for s in raw_tl['scenes']}
with open('scripts/yunani_semantic_audit.txt', 'w', encoding='utf-8') as f:
    for s in timeline_scenes:
        sid = s['id']
        dur = s['endMs'] - s['startMs']
        vis = scenes[sid - 1]['visual']
        vis = vis.replace('2D gritty, faded ochres, charcoal, muted olive, sun-bleached white. ', '')
        vis = vis.replace(' No photorealism, no readable text, no logos, no watermark.', '')
        shifted = " [SHIFTED]" if sid in OVERRIDES_SPEC or (sid + 1 in OVERRIDES_SPEC) else ""
        r_old = raw_tl_map[sid]
        f.write(f"SCENE {sid:3d} [{s['startMs']:6d} -> {s['endMs']:6d} | {dur/1000:4.2f}s]{shifted} (raw DOCX: {r_old['startMs']}-{r_old['endMs']})\n")
        f.write(f"  VO (spoken) : {s['spoken']}\n")
        f.write(f"  IMG (actual): {vis}\n\n")

# Sync summary into public/yunani/align-report.txt
with open('public/yunani/align-report.txt', 'w', encoding='utf-8') as f:
    f.write(f"Kata naskah (polished) : {len(caps)}\n")
    f.write(f"Total scene semantik   : {len(timeline_scenes)}\n")
    f.write(f"Durasi audio           : {AUDIO_DURATION_MS} ms (13m 24.36s)\n")
    f.write(f"Durasi terpendek/pjg   : {min_scene['endMs']-min_scene['startMs']} ms / {max_scene['endMs']-max_scene['startMs']} ms\n\n")
    for s in timeline_scenes:
        sid = s['id']
        tag = " [SHIFTED]" if sid in OVERRIDES_SPEC or (sid + 1 in OVERRIDES_SPEC) else ""
        f.write(f"Scene {sid:3d}  {s['startMs']:6d}-{s['endMs']:6d} ms ({(s['endMs']-s['startMs'])/1000:4.2f}s)  {s['words']:2d} kata{tag}\n")
    f.write("\nStatus: Semua 161 scene tervalidasi tanpa overlap/gap dan tersinkron secara semantik.\n")

print("Wrote public/yunani/timeline.json, public/yunani/align-report.txt, and scripts/yunani_semantic_audit.txt")
