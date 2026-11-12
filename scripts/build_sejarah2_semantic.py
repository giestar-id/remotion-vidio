import json
import shutil
import struct
from pathlib import Path

ROOT = Path(r"d:\COBA\vidio")
PUBLIC_DIR = ROOT / "public" / "sejarah-2"
VIS2_DIR = ROOT / "assets" / "sejarah islam" / "sejarah-2" / "visual2(hanya-backup)"
AUDIO_DURATION_MS = 909320


def jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:2] != b"\xff\xd8":
        raise ValueError(f"Not a JPEG: {path}")
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return (w, h)
        if marker in (0xD8, 0xD9, 0x01) or (0xD0 <= marker <= 0xD7):
            i += 2
        else:
            seg_len = struct.unpack(">H", data[i + 2 : i + 4])[0]
            i += 2 + seg_len
    raise ValueError(f"Could not find SOF frame in {path}")


def sync_clean_visuals() -> None:
    copied = 0
    for sid in range(1, 214):
        src = VIS2_DIR / f"Scene_{sid}.jpg"
        dst = PUBLIC_DIR / f"scene-{sid}.jpg"
        if not src.exists():
            raise FileNotFoundError(f"Missing {src}")
        size = jpeg_size(src)
        if size != (1376, 768):
            raise ValueError(f"Unexpected resolution in {src}: {size}")
        shutil.copy2(src, dst)
        copied += 1
    print(f"Synced {copied} clean JPEGs from visual2(hanya-backup) -> {PUBLIC_DIR}")


def polish_captions(raw_caps: list[dict], wcaps: list[dict]) -> list[dict]:
    caps = [dict(c) for c in raw_caps]
    n = len(caps)

    # 1a. Fix squeezed tokens (<= 15 ms)
    for i in range(n):
        dur = caps[i]["endMs"] - caps[i]["startMs"]
        if dur <= 15:
            if (
                i + 1 < n
                and caps[i + 1]["startMs"] == caps[i]["startMs"]
                and (caps[i + 1]["endMs"] - caps[i + 1]["startMs"]) > 80
            ):
                total_start = caps[i]["startMs"]
                total_end = caps[i + 1]["endMs"]
                l1 = max(2, len(caps[i]["text"].strip()))
                l2 = max(2, len(caps[i + 1]["text"].strip()))
                split_ms = total_start + int(round((total_end - total_start) * (l1 / (l1 + l2))))
                caps[i]["endMs"] = split_ms
                caps[i]["timestampMs"] = (total_start + split_ms) // 2
                caps[i + 1]["startMs"] = split_ms
                caps[i + 1]["timestampMs"] = (split_ms + total_end) // 2
            elif (
                i - 1 >= 0
                and (caps[i - 1]["endMs"] - caps[i - 1]["startMs"]) > 200
                and caps[i]["startMs"] == caps[i - 1]["endMs"]
            ):
                total_start = caps[i - 1]["startMs"]
                total_end = caps[i]["endMs"] + max(
                    250, (caps[i - 1]["endMs"] - caps[i - 1]["startMs"]) // 3
                )
                if i + 1 < n:
                    total_end = min(total_end, caps[i + 1]["startMs"])
                l1 = max(2, len(caps[i - 1]["text"].strip()))
                l2 = max(2, len(caps[i]["text"].strip()))
                split_ms = total_start + int(round((total_end - total_start) * (l1 / (l1 + l2))))
                caps[i - 1]["endMs"] = split_ms
                caps[i - 1]["timestampMs"] = (total_start + split_ms) // 2
                caps[i]["startMs"] = split_ms
                caps[i]["endMs"] = max(split_ms + 80, total_end)
                caps[i]["timestampMs"] = (caps[i]["startMs"] + caps[i]["endMs"]) // 2

    # 1b. Snap stretched endMs (> 900ms) where interpolated or paused before gap
    for i in range(n - 1):
        dur = caps[i]["endMs"] - caps[i]["startMs"]
        if caps[i].get("confidence") is None and dur > 900:
            cand = [w for w in wcaps if caps[i]["startMs"] <= w["startMs"] < caps[i]["endMs"] - 200]
            if cand:
                real_end = cand[-1]["endMs"]
                if real_end > caps[i]["startMs"] + 80 and real_end < caps[i]["endMs"] - 150:
                    caps[i]["endMs"] = real_end
                    caps[i]["timestampMs"] = (caps[i]["startMs"] + real_end) // 2

    # 1c. Natural documentary subtitle pageBreakAfter
    for c in caps:
        c.pop("pageBreakAfter", None)
    page_word_count = 0
    for i in range(n):
        txt = caps[i]["text"].strip()
        page_word_count += 1
        next_gap = (caps[i + 1]["startMs"] - caps[i]["endMs"]) if i + 1 < n else 9999
        is_sentence_end = txt.endswith((".", "?", "!", ":"))
        is_comma = txt.endswith((",", ";"))
        curr_clean = txt.lower().strip('“”"\'').rstrip(".,:;?!")
        next_clean = (
            caps[i + 1]["text"].strip().lower().strip('“”"\'').rstrip(".,:;?!")
            if i + 1 < n
            else ""
        )

        protected_pair = (
            (curr_clean in ("nabi", "kaum", "bani", "suku", "gua", "bukit", "kota", "masjid", "piagam", "bai'at", "baiat", "tahun"))
            or (curr_clean in ("abu", "ali", "bilal", "zaid", "ja'far", "mu'adz", "sa'ad", "abdurrahman", "kharijah", "amul", "darul", "darun", "syi'b", "ahlus", "madinatun", "al-arqam"))
            or (curr_clean in ("bin", "binti", "ibn", "di", "ke", "dari") and next_clean != "")
            or (curr_clean in ("sebelum", "610", "622") and next_clean == "masehi")
            or (curr_clean == "sahl" and next_clean == "dan")
            or (curr_clean == "aus" and next_clean == "dan")
            or (curr_clean == "laut" and next_clean == "merah")
            or (curr_clean == "konstitusi" and next_clean == "madinah")
            or (curr_clean == "pra-islam")
        )

        should_break = False
        if is_sentence_end or next_gap >= 320:
            should_break = True
        elif is_comma and page_word_count >= 5:
            should_break = True
        elif page_word_count >= 8 and not protected_pair:
            should_break = True

        if should_break and i < n - 1:
            caps[i]["pageBreakAfter"] = True
            page_word_count = 0

    return caps


def find_word_idx(caps: list[dict], phrase_words: list[str], approx_word_idx: int) -> int:
    target = [w.lower().strip('“”"\'').rstrip(".,:;?!") for w in phrase_words]
    length = len(target)
    best = None
    best_dist = 999999
    lo = max(0, approx_word_idx - 55)
    hi = min(len(caps) - length + 1, approx_word_idx + 55)
    for idx in range(lo, hi):
        seq = [
            caps[idx + k]["text"].strip().lower().strip('“”"\'').rstrip(".,:;?!")
            for k in range(length)
        ]
        if seq == target:
            d = abs(idx - approx_word_idx)
            if d < best_dist:
                best_dist = d
                best = idx
    if best is None:
        near = [caps[i]["text"].strip() for i in range(max(0, approx_word_idx - 15), min(len(caps), approx_word_idx + 20))]
        raise ValueError(f"Could not find phrase {phrase_words} near word {approx_word_idx}. Nearby={near}")
    return best


def main() -> None:
    sync_clean_visuals()

    with open(PUBLIC_DIR / "captions.json", encoding="utf-8") as f:
        raw_caps = json.load(f)
    with open(PUBLIC_DIR / "captions.whisper.json", encoding="utf-8") as f:
        wcaps = json.load(f)
    with open(PUBLIC_DIR / "scenes.json", encoding="utf-8") as f:
        scenes = json.load(f)
    with open(PUBLIC_DIR / "timeline.json", encoding="utf-8") as f:
        raw_tl = json.load(f)

    # Restore exact captions from whisper if captions.json had previous polish?
    # Note: raw_caps word count & ordering equals scenes sum (1800 words).
    caps = polish_captions(raw_caps, wcaps)
    with open(PUBLIC_DIR / "captions.json", "w", encoding="utf-8") as f:
        json.dump(caps, f, ensure_ascii=False, indent=2)

    zero_durs = [c for c in caps if c["endMs"] <= c["startMs"] or (c["endMs"] - c["startMs"]) < 40]
    print(f"Polished captions.json: {len(caps)} words, tokens <40ms: {len(zero_durs)}")

    raw_ranges = []
    cursor = 0
    for sc in scenes:
        w_count = len(sc["script"].split())
        raw_ranges.append((sc["id"], cursor, cursor + w_count - 1))
        cursor += w_count
    assert cursor == len(caps), f"Word count mismatch: {cursor} vs {len(caps)}"

    with open(ROOT / "scripts" / "sejarah2_indexed_words.txt", "w", encoding="utf-8") as f:
        for idx, c in enumerate(caps):
            f.write(f"{idx:4d} [{c['startMs']:6d}-{c['endMs']:6d}] {c['text'].strip()}\n")

    start_words = {sc["id"]: raw_ranges[sc["id"] - 1][1] for sc in scenes}

    # Exact semantic start phrases for every boundary needing alignment fix
    OVERRIDES_SPEC = {
        3: ["seseorang", "berusia", "empat", "puluh"],                  # 40yo Prophet in cave (avoid mid-phrase cut)
        4: ["Di", "bawah", "gua", "itu,"],                              # Makkah Jahiliyah valley opens cleanly
        10: ["Detik", "itu", "menjadi", "titik", "tolak"],              # Iqra finishes on S009!
        11: ["perubahan", "terbesar", "dalam", "sejarah"],              # endless desert dunes sunrise
        12: ["Bagaimana", "sebuah", "risalah", "yang"],                 # Mount Nur dawn solitary ridge
        13: ["mampu", "mengubah", "masyarakat", "yang"],                # keep "mampu" attached to conceptual split!
        14: ["hingga", "berhasil", "mendirikan", "negara-kota"],        # Madinah oasis city-state
        15: ["dalam", "rentang", "sekitar", "dua", "belas"],            # 12 golden markers timeline!
        16: ["Saat", "wahyu", "pertama", "turun,"],                     # Quraysh merchants in Makkah
        18: ["dan", "jalur", "perdagangan", "kafilah."],                # merchant camel caravan!
        19: ["Tatanan", "sosial", "di", "sana", "sangat"],              # wealthy merchant hoarding coins
        20: ["sementara", "budak", "dan", "fakir"],                     # poor enslaved workers carrying stones
        22: ["Siapa", "yang", "berasal", "dari", "klan"],               # vulnerable family from weak clan
        24: ["ketika", "Nabi", "Muhammad", "shallallahu"],              # avoid "Nabi | Muhammad" split!
        25: ["mulai", "menyuarakan", "ajaran", "tauhid"],               # clay water bowl & broken chains = tauhid/justice
        26: ["Pada", "mulanya,", "dakwah", "Islam"],                    # twilight silhouettes going secretly
        27: ["Pertemuan", "digelar", "di", "rumah"],                    # exterior Darul Arqam house!
        30: ["sebagian", "besar", "adalah", "mereka"],                  # avoid "adalah | mereka" split
        33: ["Namun", "pergerakan", "sunyi", "itu"],                    # Darul Arqam door opening to dawn hills
        34: ["saat", "perintah", "dakwah", "terang-terangan"],          # winds sweeping Bukit Safa ridge
        36: ["kepada", "kaum", "Quraisy", "yang"],                      # crowd looking up at Bukit Safa
        38: ["kepada", "kabilah-kabilah", "yang", "datang"],            # pilgrim caravans arriving at Hajj!
        40: ["Para", "sejarawan", "menganalisis", "setidaknya"],          # mapped to IMG#41 (Scholars analyzing) >= 2.1s
        41: ["lima", "alasan", "mendasar", "di", "balik"],              # mapped to IMG#40 (Parchment with 5 marks!) >= 3.2s
        42: ["Pertama,", "mereka", "menolak", "keyakinan"],             # "penolakan mereka." finishes on S041!
        43: ["dan", "pembalasan", "amal.", "Kedua,"],                   # balance of deeds -> political rivalry intro
        44: ["menyamakan", "risalah", "kenabian", "dengan"],            # rival tribal leaders arguing over seat
        46: ["menyerahkan", "kepemimpinan", "Makkah", "kepada"],        # Bani Hasyim emblem banner
        47: ["Ketiga,", "faktor", "ekonomi."],                          # Ka'bah with 360 idols!
        48: ["Kota", "Makkah", "hidup", "dari", "peziarah"],            # pilgrim caravans arriving at city gates
        49: ["dan", "orang-orang", "yang", "bergantung"],               # pagan artisan carving idols (>= 3.4s)
        50: ["takut", "kehilangan", "mata", "pencaharian"],             # anxious merchant empty coin box (>= 2.4s)
        52: ["Keempat,", "Islam", "menegaskan", "persamaan"],           # master & slave standing equal!
        53: ["hal", "yang", "sangat", "dibenci", "kaum"],               # aristocratic elder scowling in disgust
        62: ["Sebagian", "sahabat", "diperintahkan", "menyeberangi"],   # sailing dhow across Red Sea!
        64: ["Inilah", "salah", "satu", "peristiwa", "suaka"],          # refugees before King Najasyi
        65: ["lintas", "benua", "paling", "awal"],                      # Red Sea -> Africa parchment map
        70: ["Karena", "jalan", "bujukan", "gagal,"],                   # "Semua tawaran itu ditolak." stays on S069!
        71: ["piagam", "pemboikotan", "ekonomi", "dan"],                # iron seal stamped on boycott scroll
        74: ["di", "sebuah", "lembah", "sempit"],                       # keep "terkurung" inside S073 gorge
        76: ["tidak", "ada", "pernikahan", "yang"],                     # merchant caravan turning away
        77: ["Tangis", "anak-anak", "kecil", "yang"],                   # mother comforting hungry children
        78: ["menyayat", "hati", "hingga", "ke"],                       # distant illuminated houses of Makkah
        81: ["dari", "seluruh", "perjuangan", "di", "Makkah"],          # leafless desert shrub on cliff
        83: ["dua", "benteng", "pelindung", "terkuat"],                 # "Tak lama setelah boikot berakhir," plays alone on S082 scroll!
        85: ["Selang", "beberapa", "waktu", "kemudian,"],               # finish "meninggal dunia." on Abu Thalib protection
        88: ["Tanpa", "perlindungan", "Abu", "Thalib"],                 # "atau Tahun Duka Cita." stays on Amul Huzni cloud S087!
        90: ["ke", "kota", "pegunungan", "Thaif."],                     # or include "mencari basis perlindungan baru"? check dur!
        94: ["fajar", "pertolongan", "justru", "terbit"],               # beam of dawn light! ("Di tengah kepedihan..." on S093)
        96: ["Pada", "tahun", "kesebelas", "kenabian,"],                # night camel rider at Mina ("ke Makkah." stays on S095)
        98: ["Yatsrib", "adalah", "lembah", "pertanian"],               # finish "yang datang dari kota Yatsrib." on S097
        100: ["Warga", "Yatsrib", "kerap", "mendengar"],                # finish "antara suku Aus dan Khazraj." on S099
        107: ["Setahun", "berselang,", "datang", "rombongan"],          # finish "moralitas luhur." on S106
        108: ["dalam", "Bai'at", "Aqabah", "Kedua."],                   # Bai'at Aqabah II scene (>= 3.1s)
        109: ["warga", "Yatsrib", "mengundang", "Nabi"],                # tribal leaders pledging side by side (>= 3.7s)
        112: ["Nabi", "memerintahkan", "para", "pengikutnya"],          # Prophet advising discreet migration
        116: ["Menyadari", "kota", "Yatsrib", "akan"],                  # finish "di Yatsrib." inside S115!
        117: ["bagi", "umat", "Islam,", "para", "pemimpin"],            # shocked nobles (>= 2.7s)
        118: ["Pada", "tahun", "622", "Masehi,"],                       # Darun Nadwah facade
        119: ["dan", "menyusun", "rencana", "pamungkas:"],              # Darun Nadwah panicked council
        120: ["dengan", "pemuda-pemuda", "dari", "berbagai"],           # warriors ring with swords
        121: ["dituntut", "balas", "oleh", "satu"],                     # blood feud banner
        122: ["lalu", "membunuh", "beliau", "di"],                      # surrounded house at night
        123: ["Namun", "rencana", "itu", "gagal."],                     # Ali sleeping on Prophet's bed
        124: ["untuk", "mengecoh", "para", "pengepung,"],               # slipping past guards
        125: ["berhasil", "keluar", "dari", "kepungan"],                # Gua Tsur spiderweb
        126: ["lalu", "melintasi", "gurun", "menuju"],                  # riders on camels toward Yatsrib
        127: ["Sebagian", "orang", "mengira", "hijrah"],                # soldiers inspecting empty campsite!
        128: ["Padahal", "fakta", "sejarah", "membuktikan"],            # balances of conquest vs enlightenment
        129: ["Para", "pakar", "sejarah", "mencatat"],                  # ancient chronicle book!
        131: ["Hijrah", "adalah", "lompatan", "raksasa"],               # "di atas peta." stays inside S130!
        134: ["Ketika", "Nabi", "tiba", "di", "Yatsrib"],               # glowing sunrise Madinah ("dan iman." inside S133)
        135: ["beliau", "membiarkan", "untanya", "berjalan"],           # riding camel into Yatsrib in 622 CE
        137: ["Unta", "itu", "akhirnya", "berlutut"],                   # camel kneeling on date field!
        138: ["milik", "dua", "anak", "yatim"],                         # Sahl & Suhail orphan boys!
        139: ["Di", "tanah", "inilah", "kelak"],                        # foundation boundary stones
        140: ["Sejak", "itu", "Yatsrib", "dikenal"],                    # carved monument Madinatun Nabi!
        141: ["atau", "disingkat", "Madinah,", "yang"],                 # Madinah city gates
        142: ["Kata", "tamaddun,", "yang", "berarti"],                  # vine linguistic roots Tamaddun
        143: ["sehingga", "Madinah", "kerap", "dimaknai"],              # rooftops sunlight city where civilization is built
        148: ["Untuk", "membangun", "masyarakat", "majemuk"],           # "dan kepala negara-kota." stays on S147!
        152: ["untuk", "membanggakan", "garis", "keturunan."],          # check dur!
        157: ["serta", "tempat", "belajar", "bagi"],                    # Ahlus Suffah terrace starts cleanly on learning!
        160: ["antara", "kaum", "Muhajirin", "pendatang"],              # avoid "kaum | Muhajirin" split
        162: ["karena", "sebagian", "besar", "harta"],                  # confiscated houses
        173: ["Pilar", "ketiga", "adalah", "Piagam", "Madinah,"],       # Piagam Madinah scroll!
        177: ["serta", "suku-suku", "Yahudi", "seperti"],               # avoid "masih | menyembah" split!
        178: ["Piagam", "ini", "menegaskan", "bahwa"],                  # delegates around treaty table!
        184: ["berkewajiban", "bahu-membahu", "mempertahankan", "kota."],# defenders digging trench / barricade
        185: ["Tidak", "ada", "klan", "yang", "boleh"],                 # closed wooden city gate blocking covert envoys
        186: ["Dan", "jika", "terjadi", "perselisihan", "besar,"],      # two clan elders presenting disputed stone
        187: ["kepada", "Nabi", "Muhammad", "untuk"],                   # Prophet arbitrating with scroll
        188: ["Melalui", "Piagam", "Madinah,", "kelompok-kelompok"],    # Jewish elders holding pact
        193: ["dan", "mereka", "juga", "masih"],                        # avoid "bahasa | zaman sekarang" split
        195: ["Perbedaan", "corak", "sosial", "antara"],                # Split Makkah dark vs Madinah oasis!
        196: ["Di", "Makkah", "Jahiliyah,", "hukum", "rimba"],          # warlord law of the jungle ("nyata." in S195!)
        200: ["karena", "dipandang", "sebagai", "aib."],                # check dur!
        208: ["berangsur-angsur", "diarahkan", "menuju"],               # consultative assembly ("antarsuku..." in S207!)
        211: ["Dari", "satu", "orang", "yang", "menerima"],             # single oil lamp in Gua Hira ("melahirkan..." in S210!)
        212: ["lahirlah", "sebuah", "masyarakat", "yang"],              # Mount Nur golden morning beacon (>= 2.0s)
    }

    for sid, phrase in OVERRIDES_SPEC.items():
        start_words[sid] = find_word_idx(caps, phrase, start_words[sid])

    # Swap IMG#40 and IMG#41 cleanly via asset filename override
    IMAGE_OVERRIDES = {
        40: "sejarah-2/scene-41.jpg",
        41: "sejarah-2/scene-40.jpg",
    }

    for sid in range(1, 213):
        if start_words[sid] >= start_words[sid + 1]:
            raise ValueError(
                f"Non-monotonic start: Scene {sid} ({start_words[sid]}) >= Scene {sid + 1} ({start_words[sid + 1]})"
            )

    timeline_scenes = []
    for sid in range(1, 214):
        w_start = start_words[sid]
        w_end = (start_words[sid + 1] - 1) if sid < 213 else (len(caps) - 1)
        start_ms = 0 if sid == 1 else timeline_scenes[-1]["endMs"]

        if sid == 213:
            end_ms = AUDIO_DURATION_MS
        else:
            last_w_end = caps[w_end]["endMs"]
            next_w_start = caps[w_end + 1]["startMs"]
            gap = next_w_start - last_w_end
            if gap >= 260:
                cut_ms = max(last_w_end + 50, next_w_start - 130)
            elif gap >= 80:
                cut_ms = (last_w_end + next_w_start) // 2
            else:
                cut_ms = max(last_w_end - 20, next_w_start - 60)
            end_ms = int(round(cut_ms))

        spoken_text = " ".join(caps[k]["text"].strip() for k in range(w_start, w_end + 1))
        timeline_scenes.append(
            {
                "id": sid,
                "startMs": start_ms,
                "endMs": end_ms,
                "image": IMAGE_OVERRIDES.get(sid, f"sejarah-2/scene-{sid}.jpg"),
                "words": w_end - w_start + 1,
                "spoken": spoken_text,
            }
        )

    min_scene = min(timeline_scenes, key=lambda s: s["endMs"] - s["startMs"])
    max_scene = max(timeline_scenes, key=lambda s: s["endMs"] - s["startMs"])
    short_scenes = [
        (s["id"], s["endMs"] - s["startMs"], s["spoken"])
        for s in timeline_scenes
        if (s["endMs"] - s["startMs"]) < 1800
    ]
    print(f"Built {len(timeline_scenes)} semantic scenes. Total audio: {AUDIO_DURATION_MS} ms")
    print(f"Shortest scene: #{min_scene['id']} = {min_scene['endMs'] - min_scene['startMs']} ms ({min_scene['spoken']!r})")
    print(f"Longest  scene: #{max_scene['id']} = {max_scene['endMs'] - max_scene['startMs']} ms")
    print(f"Scenes < 1800ms ({len(short_scenes)}): {short_scenes}")

    clean_tl_scenes = [
        {
            "id": s["id"],
            "startMs": s["startMs"],
            "endMs": s["endMs"],
            "image": s["image"],
            "words": s["words"],
        }
        for s in timeline_scenes
    ]
    with open(PUBLIC_DIR / "timeline.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "audioDurationMs": AUDIO_DURATION_MS,
                "audio": "sejarah-2/voiceover.wav",
                "scenes": clean_tl_scenes,
            },
            f,
            indent=2,
        )

    raw_tl_map = {s["id"]: s for s in raw_tl["scenes"]}
    with open(ROOT / "scripts" / "sejarah2_semantic_audit.txt", "w", encoding="utf-8") as f:
        for s in timeline_scenes:
            sid = s["id"]
            dur = s["endMs"] - s["startMs"]
            img_num = int(s["image"].split("scene-")[1].split(".")[0])
            vis = scenes[img_num - 1]["visual"]
            shifted = " [SHIFTED]" if sid in OVERRIDES_SPEC or (sid + 1 in OVERRIDES_SPEC) else ""
            swapped = f" [USES SCENE_{img_num}]" if img_num != sid else ""
            r_old = raw_tl_map[sid]
            f.write(
                f"SCENE {sid:3d} [{s['startMs']:6d} -> {s['endMs']:6d} | {dur/1000:4.2f}s]{shifted}{swapped} (raw DOCX: {r_old['startMs']}-{r_old['endMs']})\n"
            )
            f.write(f"  VO (spoken) : {s['spoken']}\n")
            f.write(f"  IMG (actual): {vis[:155]}\n\n")

    with open(PUBLIC_DIR / "align-report.txt", "w", encoding="utf-8") as f:
        f.write(f"Kata naskah (polished) : {len(caps)}\n")
        f.write(f"Total scene semantik   : {len(timeline_scenes)}\n")
        f.write(f"Durasi audio           : {AUDIO_DURATION_MS} ms (15m 09.32s)\n")
        f.write(
            f"Durasi terpendek/pjg   : {min_scene['endMs'] - min_scene['startMs']} ms / {max_scene['endMs'] - max_scene['startMs']} ms\n\n"
        )
        for s in timeline_scenes:
            sid = s["id"]
            tag = " [SHIFTED]" if sid in OVERRIDES_SPEC or (sid + 1 in OVERRIDES_SPEC) else ""
            f.write(
                f"Scene {sid:3d}  {s['startMs']:6d}-{s['endMs']:6d} ms ({(s['endMs']-s['startMs'])/1000:4.2f}s)  {s['words']:2d} kata{tag}\n"
            )
        f.write("\nStatus: Semua 213 scene tervalidasi tanpa overlap/gap dan tersinkron secara semantik.\n")

    print("Wrote timeline.json, align-report.txt, and scripts/sejarah2_semantic_audit.txt")


if __name__ == "__main__":
    main()
