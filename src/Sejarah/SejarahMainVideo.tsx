import React from 'react';
import {AbsoluteFill, Audio, staticFile} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import type {TransitionPresentation} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import type {Caption} from '@remotion/captions';
import {SejarahScene} from './SejarahScene';
import {SejarahCaptions, SejarahDecorations} from './SejarahCaptions';
import {FPS} from '../Root';
import type {Timeline} from '../types';

const TRANSITION_FRAMES = 15; // 0,5 detik pada 30 fps

// Dominan fade; wipe/slide hanya sesekali saat pergantian topik, tidak 3x berturut-turut
const PRESENTATIONS: Array<() => TransitionPresentation<any>> = [
  () => fade(),
  () => fade(),
  () => fade(),
  () => slide({direction: 'from-right'}),
  () => fade(),
  () => fade(),
  () => wipe({direction: 'from-left'}),
  () => fade(),
];

const BASE_BG = '#241F1A';

export const SejarahDocu: React.FC<{
  proyek: string;
  timeline: Timeline | null;
  captions: Caption[];
}> = ({timeline, captions}) => {
  if (!timeline) return null;

  // Batas scene dalam frame (kumulatif, dibulatkan sekali agar tidak drift)
  const boundaries = timeline.scenes.map((s) => Math.round((s.startMs / 1000) * FPS));
  const total = Math.round((timeline.audioDurationMs / 1000) * FPS);
  boundaries.push(total);

  const base = boundaries.slice(0, -1).map((b, i) => boundaries[i + 1] - b);

  // Transisi keluar tiap scene: tidak boleh melebihi setengah durasi scene di sekitarnya
  const tFrames = base.map((d, i) => {
    if (i === base.length - 1) return 0;
    return Math.max(0, Math.min(TRANSITION_FRAMES, Math.floor(d / 2), Math.floor(base[i + 1] / 2)));
  });

  return (
    <AbsoluteFill style={{backgroundColor: BASE_BG}}>
      <Audio src={staticFile(timeline.audio)} />

      <TransitionSeries>
        {timeline.scenes.flatMap((scene, i) => {
          const duration = base[i] + tFrames[i]; // diperpanjang sebesar transisi keluar
          const items = [
            <TransitionSeries.Sequence
              key={`s-${scene.id}`}
              durationInFrames={duration}
            >
              <SejarahScene
                src={staticFile(scene.image)}
                index={i}
                durationInFrames={duration}
              />
            </TransitionSeries.Sequence>,
          ];
          if (tFrames[i] > 0) {
            items.push(
              <TransitionSeries.Transition
                key={`t-${scene.id}`}
                presentation={PRESENTATIONS[i % PRESENTATIONS.length]()}
                timing={linearTiming({durationInFrames: tFrames[i]})}
              />,
            );
          }
          return items;
        })}
      </TransitionSeries>

      <SejarahCaptions captions={captions} />
      <SejarahDecorations />
    </AbsoluteFill>
  );
};
