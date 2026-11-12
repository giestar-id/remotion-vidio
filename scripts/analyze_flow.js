import fs from 'node:fs';

const scenes = JSON.parse(fs.readFileSync('public/stickman/scenes.json', 'utf8'));
const timeline = JSON.parse(fs.readFileSync('public/stickman/timeline.json', 'utf8'));
const captions = JSON.parse(fs.readFileSync('public/stickman/captions.json', 'utf8'));

let wordIdx = 0;
for (let i = 0; i < 25; i++) {
  const sc = scenes[i];
  const tl = timeline.scenes[i];
  const words = sc.script.split(/\s+/).filter(Boolean);
  const scCaps = captions.slice(wordIdx, wordIdx + words.length);
  wordIdx += words.length;

  const firstCap = scCaps[0];
  const lastCap = scCaps[scCaps.length - 1];
  
  // Extract visual idea from prompt
  const match = sc.visual.match(/Visual idea:\s*([^.]+)\./i);
  const visualIdea = match ? match[1] : sc.visual.slice(0, 80);

  console.log(`\n[Scene ${String(sc.id).padStart(2)}] (${tl.startMs} - ${tl.endMs} ms | ${((tl.endMs - tl.startMs)/1000).toFixed(2)}s)`);
  console.log(`  Script : "${sc.script}"`);
  console.log(`  Visual : ${visualIdea}`);
  console.log(`  Words  : "${firstCap.text.trim()}" (${firstCap.startMs}ms) -> "${lastCap.text.trim()}" (${lastCap.endMs}ms)`);
}

