import json

with open('public/yunani/captions.whisper.json', encoding='utf-8') as f:
    wc = json.load(f)

def show_window(lo, hi):
    print(f'--- Window {lo}..{hi} ms ---')
    for w in wc:
        if lo <= w['startMs'] <= hi:
            print(f"  {w['startMs']:6d} - {w['endMs']:6d} : {w['text']!r}")

show_window(22000, 34000)
show_window(132000, 142000)
show_window(262000, 276000)
show_window(280000, 293000)
show_window(335000, 349000)
show_window(553000, 572000)
show_window(584000, 615000)
show_window(664000, 678000)
show_window(696000, 731000)
show_window(753000, 791000)

