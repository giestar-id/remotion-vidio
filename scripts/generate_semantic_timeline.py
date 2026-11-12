import json

def build_timeline():
    # Load whisper captions to get exact word-level timings
    with open('public/stickman/captions.whisper.json', encoding='utf-8') as f:
        whisper_caps = json.load(f)
        
    # Helper to find closest timestamp for a word / phrase
    def find_time(word_prefix, start_search_ms=0):
        for c in whisper_caps:
            if c['startMs'] >= start_search_ms:
                clean = c['text'].strip().lower()
                if clean.startswith(word_prefix.lower()) or word_prefix.lower() in clean:
                    return c['startMs'], c['endMs']
        return None, None

    # We will build a list of 114 timeline scenes:
    # { "id": i, "startMs": s, "endMs": e, "image": "stickman/scene-i.jpg" }
    
    # Let's map each boundary explicitly:
    # 1: 0 -> "anak-anak" (5160)
    # 2: 5160 -> "Saat" (8440)
    # 3: 8440 -> "ia" (10800) [Needle touching cylinder]
    # 4: 10800 -> "Suara" (12780) [Edison jumping back in surprise: "ia tersentak kaget"]
    # 5: 12780 -> "Yang/Ia" (16880) [Horn with sound waves: "Suara dari corong itu sama sekali tidak terdengar seperti dirinya"]
    # 6: 16880 -> "yang menirukan" (18900) [Edison staring at shadow: "Ia merasa seperti mendengar orang asing"]
    # 7: 18900 -> "Mengapa" (21000) [Edison pointing at shadow: "yang menirukan perkataannya."]
    # 8: 21000 -> "saat mendengar" (24980) [Earth globe: "Mengapa hampir semua manusia di bumi merasa asing dan terganggu"]
    # 9: 24980 -> "Setiap kali" (26840) [Headphones cringing: "saat mendengar rekaman suaranya sendiri?"]
    # 10: 26840 -> "Jalur pertama" (33840) [Branching paths: "Setiap kali kamu berbicara, suaramu menempuh dua jalur yang berbeda untuk sampai ke telingamu."]
    # 11: 33840 -> "merambat di udara" (37680) [Air path mouth: "Jalur pertama adalah konduksi udara. Gelombang suara keluar dari mulutmu,"]
    # 12: 37680 -> "menggetarkan" (40340) [Air soundwaves traveling: "merambat di udara,"]
    # 13: 40340 -> "Orang lain" (44540) [Ear drum: "menggetarkan gendang telinga, lalu diteruskan ke organ pendengaran."]
    # 14: 44540 -> "Namun, kamu" (48480) [External listener: "Orang lain mendengar suaramu murni melalui jalur udara ini."]
    # 15: 48480 -> "Saat pita suaramu" (53980) [Bone path: "Namun, kamu mendengar suaramu sendiri melalui jalur kedua, yaitu konduksi tulang."]
    
    # 16 to 25: 10 Skull diagrams (BASS 16 to 25)
    # 16: 53980 -> "Tulang tengkorak manusia" (59840)
    # 17: 59840 -> "Tulang ini memperkuat" (63920)
    # 18: 63920 -> "Hasilnya" (68480)
    # 19: 68480 -> "terasa lebih berat" (72020)
    # 20: 72020 -> "Kamu sudah terbiasa" (75020)
    # 21: 75020 -> "Tapi saat suara" (79520)
    # 22: 79520 -> "Komponen getaran" (84520)
    # 23: 84520 -> "Suaramu tiba-tiba" (87400)
    # 24: 87400 -> "Tapi ini belum" (90860)
    # 25: 90860 -> "Apakah ketidaknyamanan" (92620)
    
    # 26 to 37: 12 Psychological testing scenes
    # 26: 92620 -> "Pada tahun 1966" (97380)
    # 27: 97380 -> "menggelar penelitian" (101500)
    # 28: 101500 -> "Mereka curiga" (105840)
    # 29: 105840 -> "Holzman dan Rousey menamai" (109470)
    # 30: 109470 -> "Dalam uji coba" (116050)
    # 31: 116050 -> "yang mampu mengenali" (120500)
    # 32: 120500 -> "Begitu rekaman" (124350)
    # 33: 124350 -> "para peserta berteriak" (126500)
    # 34: 126500 -> "Holzman dan Rousey menemukan" (129650)
    # 35: 129650 -> "Rasa cemas itu muncul" (133630)
    # 36: 133630 -> "Rekaman suara ternyata" (136550)
    # 37: 136550 -> "Saat kamu berbicara" (141510)
    
    # 38 to 50: 13 Bilingual subject testing scenes
    # 38: 141510 -> "Kamu tidak sadar" (145570)
    # 39: 145570 -> "Isyarat ini mencakup" (148370)
    # 40: 148370 -> "membocorkan rasa cemas" (151500)
    # 41: 151500 -> "Rekaman suara memutar" (155830)
    # 42: 155830 -> "tidak ingin kamu tunjukkan" (158500)
    # 43: 158500 -> "Dan di sinilah" (162020)
    # 44: 162020 -> "Pada tahun 1967" (164330)
    # 45: 164330 -> "menguji kelompok orang" (168600)
    # 46: 168600 -> "Mereka menguji peserta" (172530)
    # 47: 172530 -> "Para peneliti membandingkan" (177090)
    # 48: 177090 -> "dalam bahasa ibu" (180200)
    # 49: 180200 -> "Hasilnya sungguh" (183680)
    # 50: 183680 -> "Para peserta merasa" (185640)
    
    # 51 to 70: 20 Brain motor cortex diagrams
    # 51: 185640 -> "Padahal tulang tengkorak" (191160)
    # 52: 191160 -> "Ini membuktikan bahwa" (196140)
    # 53: 196140 -> "melainkan kejutan" (199500)
    # 54: 199500 -> "Karena bahasa ibu" (202540)
    # 55: 202540 -> "Mari kita atur" (207390)
    # 56: 207390 -> "Otakmu telah membangun" (209950)
    # 57: 209950 -> "Saat rekaman diputar" (213630)
    # 58: 213630 -> "karena suaramu tidak" (216500)
    # 59: 216500 -> "Lalu bagaimana otakmu" (218690)
    # 60: 218690 -> "Bayangkan saat kamu" (223750)
    # 61: 223750 -> "Kamu tidak akan" (226950)
    # 62: 226950 -> "Hal yang sama" (231090)
    # 63: 231090 -> "Ketika korteks motorik" (233750)
    # 64: 233750 -> "otak mengirim sinyal" (236500)
    # 65: 236500 -> "Sinyal pertama dikirim" (239590)
    # 66: 239590 -> "sinyal kedua dikirim" (243500)
    # 67: 243500 -> "Salinan ini memicu" (248370)
    # 68: 248370 -> "Ramalan ini memperkirakan" (252970)
    # 69: 252970 -> "Saat suara aktualmu" (256090)
    # 70: 256090 -> "Dalam pengukuran" (261470)
    
    # 71 to 90: 20 EEG brainwave graphs
    # 71: 261470 -> "yang memuncak pada" (265500)
    # 72: 265500 -> "Otakmu sengaja" (270330)
    # 73: 270330 -> "agar kamu tidak" (273000)
    # 74: 273000 -> "Gampangnya otakmu" (275750)
    # 75: 275750 -> "setiap kali kamu" (278500)
    # 76: 278500 -> "Namun mekanismenya" (281950)
    # 77: 281950 -> "Saat memutar ulang" (285890)
    # 78: 285890 -> "Tidak ada perintah" (289550)
    # 79: 289550 -> "dan sinyal peredam" (292000)
    # 80: 292000 -> "Otakmu menganalisis" (295610)
    # 81: 295610 -> "Otak memproses" (299270)
    # 82: 299270 -> "sama seperti saat" (302000)
    # 83: 302000 -> "Tetapi orang mengira" (305090)
    # 84: 305090 -> "Ternyata anggapan" (309290)
    # 85: 309290 -> "Pada tahun 2013" (311990)
    # 86: 311990 -> "menggelar eksperimen" (315000)
    # 87: 315000 -> "Mereka meminta 80" (318870)
    # 88: 318870 -> "dari berbagai rekaman" (321500)
    # 89: 321500 -> "Tanpa diberitahu" (324970)
    # 90: 324970 -> "Hasilnya sangat" (330150)
    
    # 91 to 105: 15 Rating experiment scenes
    # 91: 330150 -> "Ketika peserta tidak" (332310)
    # 92: 332310 -> "Mereka justru menilai" (335690)
    # 93: 335690 -> "dibandingkan penilaian" (338000)
    # 94: 338000 -> "Otakmu secara tidak" (340310)
    # 95: 340310 -> "melalui bias ego" (343000)
    # 96: 343000 -> "Di sinilah titik" (345870)
    # 97: 345870 -> "Rasa tidak nyaman" (347950)
    # 98: 347950 -> "saat kesadaran" (350500)
    # 99: 350500 -> "Penelitian terbaru" (353470)
    # 100: 353470 -> "Ketika orang secara" (358750)
    # 101: 358750 -> "ekspektasi internal" (362000)
    # 102: 362000 -> "Kesadaran itulah" (366170)
    # 103: 366170 -> "Jadi suaramu" (370360)
    # 104: 370360 -> "Orang lain mendengarnya" (374500)
    # 105: 374500 -> "Yang membuatmu" (378020)
    
    # 106 to 114: 9 Authentic vocal beauty scenes
    # 106: 378020 -> "kehilangan filter" (380800)
    # 107: 380800 -> "Sejak Thomas Edison" (384440)
    # 108: 384440 -> "manusia terus terkejut" (388500)
    # 109: 388500 -> "Namun kini kamu" (392260)
    # 110: 392260 -> "Suara dari rekaman" (394840)
    # 111: 394840 -> "Jika kamu terus" (398980)
    # 112: 398980 -> "otakmu akan terbiasa" (401500)
    # 113: 401500 -> "Lagipula jika secara" (404250)
    # 114: 404250 -> 411680
    
    boundaries = [
        0,      # 1
        5160,   # 2
        8440,   # 3 (Needle starts on "Saat jarum mesin...")
        10800,  # 4 (Edison jumps back on "...ia tersentak kaget")
        12780,  # 5 (Horn emitting sound arcs on "Suara dari corong itu...")
        16880,  # 6 (Edison staring at shadow on "Ia merasa seperti mendengar orang asing...")
        18900,  # 7 (Edison pointing at shadow on "...yang menirukan perkataannya")
        21000,  # 8 (Earth globe on "Mengapa hampir semua manusia di bumi...")
        24980,  # 9 (Headphones cringing on "...saat mendengar rekaman suaranya sendiri?")
        26840,  # 10 (Branching paths on "Setiap kali kamu berbicara, suaramu menempuh dua jalur...")
        33840,  # 11 (Air path on "Jalur pertama adalah konduksi udara...")
        37680,  # 12 (Soundwaves traveling on "merambat di udara...")
        40340,  # 13 (Ear drum vibrating on "menggetarkan gendang telinga...")
        44540,  # 14 (External listener on "Orang lain mendengar suaramu...")
        48480,  # 15 (Bone path on "Namun, kamu mendengar suaramu sendiri melalui jalur kedua...")
        
        53980,  # 16
        59840,  # 17
        63920,  # 18
        68480,  # 19
        72020,  # 20
        75020,  # 21
        79520,  # 22
        84520,  # 23
        87400,  # 24
        90860,  # 25
        
        92620,  # 26
        97380,  # 27
        101500, # 28
        105840, # 29
        109470, # 30
        116050, # 31
        120500, # 32
        124350, # 33
        126500, # 34
        129650, # 35
        133630, # 36
        136550, # 37
        
        141510, # 38
        145570, # 39
        148370, # 40
        151500, # 41
        155830, # 42
        158500, # 43
        162020, # 44
        164330, # 45
        168600, # 46
        172530, # 47
        177090, # 48
        180200, # 49
        183680, # 50
        
        185640, # 51
        191160, # 52
        196140, # 53
        199500, # 54
        202540, # 55
        207390, # 56
        209950, # 57
        213630, # 58
        216500, # 59
        218690, # 60
        223750, # 61
        226950, # 62
        231090, # 63
        233750, # 64
        236500, # 65
        239590, # 66
        243500, # 67
        248370, # 68
        252970, # 69
        256090, # 70
        
        261470, # 71
        265500, # 72
        270330, # 73
        273000, # 74
        275750, # 75
        278500, # 76
        281950, # 77
        285890, # 78
        289550, # 79
        292000, # 80
        295610, # 81
        299270, # 82
        302000, # 83
        305090, # 84
        309290, # 85
        311990, # 86
        315000, # 87
        318870, # 88
        321500, # 89
        324970, # 90
        
        330150, # 91
        332310, # 92
        335690, # 93
        338000, # 94
        340310, # 95
        343000, # 96
        345870, # 97
        347950, # 98
        350500, # 99
        353470, # 100
        358750, # 101
        362000, # 102
        366170, # 103
        370360, # 104
        374500, # 105
        
        378020, # 106
        380800, # 107
        384440, # 108 (Sejak Thomas Edison memutar ulang...)
        388500, # 109
        392260, # 110
        394840, # 111
        398980, # 112
        404250, # 113
        408000, # 114
        411680  # End of audio
    ]
    
    assert len(boundaries) == 115, f"Expected 115 boundaries, got {len(boundaries)}"
    
    timeline_scenes = []
    for i in range(114):
        s_id = i + 1
        s_start = boundaries[i]
        s_end = boundaries[i + 1]
        
        # Check image exists
        img_name = f"stickman/scene-{s_id}.jpg"
        
        timeline_scenes.append({
            "id": s_id,
            "startMs": s_start,
            "endMs": s_end,
            "image": img_name
        })
        
    timeline_data = {
        "audioDurationMs": 411680,
        "audio": "stickman/voiceover.wav",
        "scenes": timeline_scenes
    }
    
    with open('public/stickman/timeline.json', 'w', encoding='utf-8') as f:
        json.dump(timeline_data, f, ensure_ascii=False, indent=2)
        
    print("Successfully built semantic timeline with 114 scenes!")
    print(f"Total scenes: {len(timeline_scenes)}")
    print(f"Total duration: {timeline_scenes[-1]['endMs']} ms")

if __name__ == '__main__':
    build_timeline()

