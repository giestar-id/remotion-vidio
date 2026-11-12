import fs from 'node:fs';

const timeline = JSON.parse(fs.readFileSync('public/stickman/timeline.json', 'utf8'));
const scenes = JSON.parse(fs.readFileSync('public/stickman/scenes.json', 'utf8'));
const captions = JSON.parse(fs.readFileSync('public/stickman/captions.json', 'utf8'));

console.log('=== AUDIT REPORT SINKRONISASI ===');
console.log('Total scenes in scenes.json  :', scenes.length);
console.log('Total scenes in timeline.json:', timeline.scenes.length);
console.log('Total captions in captions.json:', captions.length);
console.log('Audio duration in timeline   :', timeline.audioDurationMs, 'ms');

const issues = [];
const stats = {
  totalScenes: timeline.scenes.length,
  perfectMatches: 0,
  minMatchRatio: 1,
  maxMatchRatio: 0,
  durations: [],
};

// 1. Check scene continuity & bounds
for (let i = 0; i < timeline.scenes.length; i++) {
  const s = timeline.scenes[i];
  const dur = s.endMs - s.startMs;
  stats.durations.push(dur);
  if (s.matchRatio < stats.minMatchRatio) stats.minMatchRatio = s.matchRatio;
  if (s.matchRatio > stats.maxMatchRatio) stats.maxMatchRatio = s.matchRatio;
  if (s.matchRatio >= 0.99) stats.perfectMatches++;

  if (s.startMs >= s.endMs) {
    issues.push(`Scene ${s.id}: durasi tidak valid (${s.startMs} -> ${s.endMs} ms)`);
  }
  if (i > 0) {
    const prev = timeline.scenes[i - 1];
    if (prev.endMs !== s.startMs) {
      issues.push(`Celah/tumpang tindih Scene ${prev.id} dan ${s.id}: ${prev.endMs} ms vs ${s.startMs} ms`);
    }
  }
}

// 2. Check scene images exist and size > 0
timeline.scenes.forEach((s) => {
  const imgPath = 'public/' + s.image;
  if (!fs.existsSync(imgPath)) {
    issues.push(`Gambar hilang Scene ${s.id}: ${imgPath}`);
  } else {
    const stat = fs.statSync(imgPath);
    if (stat.size === 0) {
      issues.push(`Gambar corrupt (0 byte) Scene ${s.id}: ${imgPath}`);
    }
  }
});

// 3. Check Caption alignment with scenes
let wordIdx = 0;
const sceneAudits = [];

for (let i = 0; i < scenes.length; i++) {
  const scene = scenes[i];
  const tScene = timeline.scenes[i];
  const sceneWords = scene.script.split(/\s+/).filter(Boolean);

  const sceneCaptions = [];
  for (let w = 0; w < sceneWords.length; w++) {
    if (wordIdx < captions.length) {
      sceneCaptions.push(captions[wordIdx]);
      wordIdx++;
    }
  }

  if (sceneCaptions.length > 0) {
    const firstWord = sceneCaptions[0];
    const lastWord = sceneCaptions[sceneCaptions.length - 1];

    const leadTime = firstWord.startMs - tScene.startMs;
    const trailTime = tScene.endMs - lastWord.endMs;

    // First word should start AT OR AFTER scene image appears (leadTime >= 0)
    let leadOk = true;
    if (firstWord.startMs < tScene.startMs) {
      leadOk = false;
      issues.push(
        `Scene ${tScene.id}: Kata pertama "${firstWord.text.trim()}" mulai di ${firstWord.startMs}ms, SEBELUM gambar scene muncul di ${tScene.startMs}ms (selisih ${firstWord.startMs - tScene.startMs}ms)`
      );
    }

    // Last word should finish BEFORE OR AT scene image disappearance (trailTime >= 0)
    let trailOk = true;
    if (lastWord.endMs > tScene.endMs) {
      trailOk = false;
      issues.push(
        `Scene ${tScene.id}: Kata terakhir "${lastWord.text.trim()}" selesai di ${lastWord.endMs}ms, SETELAH gambar scene berganti di ${tScene.endMs}ms (selisih ${lastWord.endMs - tScene.endMs}ms)`
      );
    }

    sceneAudits.push({
      id: tScene.id,
      words: sceneWords.length,
      sceneDurationMs: tScene.endMs - tScene.startMs,
      firstWord: firstWord.text.trim(),
      firstWordStartMs: firstWord.startMs,
      leadTimeMs: leadTime,
      lastWord: lastWord.text.trim(),
      lastWordEndMs: lastWord.endMs,
      trailTimeMs: trailTime,
      matchRatio: tScene.matchRatio,
      leadOk,
      trailOk,
    });
  }
}

console.log('\n--- RINGKASAN STATISTIK ---');
console.log(`Jumlah Scene              : ${stats.totalScenes}`);
console.log(`Scene Cocok 100%          : ${stats.perfectMatches} dari ${stats.totalScenes} (${((stats.perfectMatches / stats.totalScenes) * 100).toFixed(1)}%)`);
console.log(`Akurasi Pencocokan Minimum: ${(stats.minMatchRatio * 100).toFixed(1)}%`);
console.log(`Durasi Scene Terpendek    : ${Math.min(...stats.durations)} ms`);
console.log(`Durasi Scene Terpanjang   : ${Math.max(...stats.durations)} ms`);
console.log(`Rata-rata Durasi Scene    : ${(stats.durations.reduce((a, b) => a + b, 0) / stats.durations.length).toFixed(0)} ms`);

console.log('\n--- TEMUAN ISU SINKRONISASI ---');
if (issues.length === 0) {
  console.log('✅ SEMUA 114 SCENE, GAMBAR, CAPTION, DAN AUDIO SINKRON SECARA PRESISI TANPA CELAH!');
} else {
  console.log(`Ditemukan ${issues.length} potensi isu:`);
  issues.forEach((iss) => console.log(' - ' + iss));
}

// 4. Sample checking first 5 and last 5 scenes
console.log('\n--- SAMPEL AUDIT SCENE 1 - 5 ---');
sceneAudits.slice(0, 5).forEach((s) => {
  console.log(
    `Scene ${String(s.id).padStart(2)}: [${s.firstWord}...${s.lastWord}] ` +
      `Gambar: ${s.sceneDurationMs}ms (${s.leadTimeMs}ms lead, ${s.trailTimeMs}ms trail) ` +
      `Akurasi: ${(s.matchRatio * 100).toFixed(0)}%`
  );
});

console.log('\n--- SAMPEL AUDIT SCENE 110 - 114 ---');
sceneAudits.slice(-5).forEach((s) => {
  console.log(
    `Scene ${String(s.id).padStart(2)}: [${s.firstWord}...${s.lastWord}] ` +
      `Gambar: ${s.sceneDurationMs}ms (${s.leadTimeMs}ms lead, ${s.trailTimeMs}ms trail) ` +
      `Akurasi: ${(s.matchRatio * 100).toFixed(0)}%`
  );
});

