#!/usr/bin/env node
/**
 * align.mjs - Menyelaraskan kata-kata naskah (dari tabel) dengan transkrip Whisper
 * untuk mendapatkan waktu mulai/selesai setiap scene.
 */
import fs from 'node:fs';
import path from 'node:path';

// ---------- argumen ----------
const args = process.argv.slice(2);
const getArg = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : fallback;
};
const scenesPath = getArg('scenes');
const captionsPath = getArg('captions');
const outDir = getArg('out-dir', path.dirname(scenesPath ?? '.'));
const LEAD_MS = Number(getArg('lead-ms', 100)); // gambar berganti sedikit SEBELUM kata pertama scene
const MIN_RATIO = Number(getArg('min-ratio', 0.6)); // di bawah ini scene dianggap mencurigakan
const publicDir = getArg('public-dir', null); // mis. "public"; bila diisi, gambar scene-N dicari otomatis
const audioFile = getArg('audio-file', null); // path audio relatif terhadap --public-dir
const SIM_THRESHOLD = 0.6; // kemiripan minimal agar sepasang kata dianggap "cocok"

if (!scenesPath || !captionsPath) {
  console.error('Wajib: --scenes <scenes.json> --captions <captions.whisper.json>');
  process.exit(1);
}

const scenes = JSON.parse(fs.readFileSync(scenesPath, 'utf8'));
const whisperCaptions = JSON.parse(fs.readFileSync(captionsPath, 'utf8'));

// ---------- util ----------
const norm = (s) =>
  s
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[^\p{L}\p{N}]/gu, '');

function levenshtein(a, b) {
  if (a === b) return 0;
  const m = a.length;
  const n = b.length;
  if (!m) return n;
  if (!n) return m;
  let prev = Array.from({length: n + 1}, (_, j) => j);
  for (let i = 1; i <= m; i++) {
    const cur = [i];
    for (let j = 1; j <= n; j++) {
      cur[j] = Math.min(
        prev[j] + 1,
        cur[j - 1] + 1,
        prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1),
      );
    }
    prev = cur;
  }
  return prev[n];
}
const similarity = (a, b) => {
  if (a === b) return 1;
  return 1 - levenshtein(a, b) / Math.max(a.length, b.length);
};

// ---------- 1. token Whisper -> kata ----------
const tWords = [];
for (const c of whisperCaptions) {
  const raw = c.text ?? '';
  if (/^\s*\[.*\]\s*$/.test(raw)) continue; // [_BEG_], [MUSIC], dsb.
  const startsNew = /^\s/.test(raw) || tWords.length === 0;
  const clean = raw.trim();
  if (!clean) continue;
  if (startsNew) {
    tWords.push({text: clean, startMs: c.startMs, endMs: c.endMs});
  } else {
    const last = tWords[tWords.length - 1];
    last.text += clean;
    last.endMs = c.endMs;
  }
}
const tNorm = tWords.map((w) => norm(w.text));

// ---------- 2. kata naskah ----------
const sWords = []; // {orig, norm, scene (index di array scenes)}
scenes.forEach((scene, si) => {
  for (const orig of String(scene.script).split(/\s+/).filter(Boolean)) {
    const n = norm(orig);
    if (n) sWords.push({orig, norm: n, scene: si});
  }
});

const audioDurationMs = Number(
  getArg('duration-ms', tWords.length ? tWords[tWords.length - 1].endMs : 0),
);

// ---------- 3. alignment global (edit distance) ----------
const N = sWords.length;
const M = tWords.length;
if (N * M > 60_000_000) {
  console.error(`Terlalu besar untuk alignment penuh (${N} x ${M}). Pecah audio/naskah per bagian.`);
  process.exit(1);
}
const GAP = 0.9;
const W = M + 1;
const dir = new Uint8Array((N + 1) * W); // 1 = diagonal, 2 = skip kata naskah, 3 = skip kata transkrip
let prevRow = new Float32Array(W);
for (let j = 1; j <= M; j++) {
  prevRow[j] = j * GAP;
  dir[j] = 3;
}
for (let i = 1; i <= N; i++) {
  const row = new Float32Array(W);
  row[0] = i * GAP;
  dir[i * W] = 2;
  for (let j = 1; j <= M; j++) {
    const sub = prevRow[j - 1] + (1 - similarity(sWords[i - 1].norm, tNorm[j - 1]));
    const skipS = prevRow[j] + GAP;
    const skipT = row[j - 1] + GAP;
    if (sub <= skipS && sub <= skipT) {
      row[j] = sub;
      dir[i * W + j] = 1;
    } else if (skipS <= skipT) {
      row[j] = skipS;
      dir[i * W + j] = 2;
    } else {
      row[j] = skipT;
      dir[i * W + j] = 3;
    }
  }
  prevRow = row;
}

// traceback
const matchOf = new Array(N).fill(-1); // indeks kata naskah -> indeks kata transkrip
{
  let i = N;
  let j = M;
  while (i > 0 || j > 0) {
    const d = dir[i * W + j];
    if (i > 0 && j > 0 && d === 1) {
      if (similarity(sWords[i - 1].norm, tNorm[j - 1]) >= SIM_THRESHOLD) matchOf[i - 1] = j - 1;
      i--;
      j--;
    } else if (i > 0 && (d === 2 || j === 0)) {
      i--;
    } else {
      j--;
    }
  }
}

// ---------- 4. waktu per kata naskah (interpolasi untuk yang tidak cocok) ----------
const times = new Array(N).fill(null);
for (let i = 0; i < N; i++) {
  if (matchOf[i] >= 0) times[i] = {startMs: tWords[matchOf[i]].startMs, endMs: tWords[matchOf[i]].endMs};
}
let i = 0;
while (i < N) {
  if (times[i]) {
    i++;
    continue;
  }
  let j = i;
  while (j < N && !times[j]) j++;
  const from = i > 0 ? times[i - 1].endMs : 0;
  const to = j < N ? times[j].startMs : Math.max(audioDurationMs, from);
  const weights = [];
  for (let k = i; k < j; k++) weights.push(sWords[k].norm.length + 1);
  const total = weights.reduce((a, b) => a + b, 0);
  let cursor = from;
  for (let k = i; k < j; k++) {
    const span = ((to - from) * weights[k - i]) / total;
    times[k] = {startMs: Math.round(cursor), endMs: Math.round(cursor + span)};
    cursor += span;
  }
  i = j;
}

// ---------- 5. batas scene ----------
const ranges = scenes.map(() => ({first: -1, last: -1}));
sWords.forEach((w, idx) => {
  const r = ranges[w.scene];
  if (r.first < 0) r.first = idx;
  r.last = idx;
});

const problems = [];
const timelineScenes = scenes.map((scene, si) => {
  const r = ranges[si];
  if (r.first < 0) {
    problems.push(`Scene ${scene.id}: naskah kosong.`);
    return {id: scene.id, startMs: 0, endMs: 0, matchRatio: 0, words: 0};
  }
  let matched = 0;
  for (let k = r.first; k <= r.last; k++) if (matchOf[k] >= 0) matched++;
  return {
    id: scene.id,
    startMs: times[r.first].startMs,
    endMs: times[r.last].endMs, // sementara; akan diganti oleh batas scene berikutnya
    firstWordStartMs: times[r.first].startMs,
    lastWordEndMs: times[r.last].endMs,
    matchRatio: Number((matched / (r.last - r.first + 1)).toFixed(3)),
    words: r.last - r.first + 1,
  };
});

for (let si = 0; si < timelineScenes.length; si++) {
  const cur = timelineScenes[si];
  if (si === 0) cur.startMs = 0; // scene pertama menutup jeda awal audio
  if (si < timelineScenes.length - 1) {
    const next = timelineScenes[si + 1];
    const boundary = Math.max(cur.lastWordEndMs ?? 0, (next.firstWordStartMs ?? 0) - LEAD_MS);
    cur.endMs = Math.round(boundary);
    next.startMs = Math.round(boundary);
  } else {
    cur.endMs = Math.round(Math.max(audioDurationMs, cur.lastWordEndMs ?? 0));
  }
}
for (const s of timelineScenes) {
  delete s.firstWordStartMs;
  delete s.lastWordEndMs;
  if (s.endMs <= s.startMs) problems.push(`Scene ${s.id}: durasi <= 0 (${s.startMs}-${s.endMs} ms).`);
  if (s.matchRatio < MIN_RATIO) problems.push(`Scene ${s.id}: kecocokan rendah (${s.matchRatio}). Cek manual.`);
}

// ---------- 5b. cari gambar scene-N (ekstensi apa pun) ----------
const IMAGE_EXTS = ['png', 'jpg', 'jpeg', 'webp'];
if (publicDir) {
  const assetsAbs = path.join(publicDir, path.dirname(audioFile ?? scenesPath.replace(publicDir + path.sep, '')));
  const searchDirs = [...new Set([assetsAbs, outDir])];
  for (const s of timelineScenes) {
    let found = null;
    for (const dirPath of searchDirs) {
      for (const ext of IMAGE_EXTS) {
        const candidate = path.join(dirPath, `scene-${s.id}.${ext}`);
        if (fs.existsSync(candidate)) {
          found = path.relative(publicDir, candidate).split(path.sep).join('/');
          break;
        }
      }
      if (found) break;
    }
    if (found) s.image = found;
    else problems.push(`Scene ${s.id}: gambar scene-${s.id}.(${IMAGE_EXTS.join('|')}) tidak ditemukan.`);
  }
}

// ---------- 6. caption memakai teks naskah ----------
const captions = sWords.map((w, idx) => ({
  text: ' ' + w.orig,
  startMs: times[idx].startMs,
  endMs: Math.max(times[idx].endMs, times[idx].startMs + 1),
  timestampMs: Math.round((times[idx].startMs + times[idx].endMs) / 2),
  confidence: matchOf[idx] >= 0 ? 1 : null,
}));

// ---------- 7. tulis ----------
fs.mkdirSync(outDir, {recursive: true});
fs.writeFileSync(
  path.join(outDir, 'timeline.json'),
  JSON.stringify({audioDurationMs, audio: audioFile ?? null, scenes: timelineScenes}, null, 2),
);
fs.writeFileSync(path.join(outDir, 'captions.json'), JSON.stringify(captions, null, 2));

const totalMatched = matchOf.filter((m) => m >= 0).length;
const report = [
  `Kata naskah     : ${N}`,
  `Kata transkrip  : ${M}`,
  `Kata cocok      : ${totalMatched} (${((totalMatched / Math.max(N, 1)) * 100).toFixed(1)}%)`,
  `Durasi audio    : ${audioDurationMs} ms`,
  '',
  ...timelineScenes.map((s) => `Scene ${String(s.id).padStart(3)}  ${s.startMs}-${s.endMs} ms  cocok ${(s.matchRatio * 100).toFixed(0)}%  (${s.words} kata)`),
  '',
  problems.length ? 'PERLU DICEK:\n- ' + problems.join('\n- ') : 'Tidak ada masalah terdeteksi.',
].join('\n');
fs.writeFileSync(path.join(outDir, 'align-report.txt'), report);
console.log(report);

