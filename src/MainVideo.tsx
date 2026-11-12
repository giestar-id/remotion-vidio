import React from 'react';
import { AbsoluteFill, Audio, staticFile } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import type { TransitionPresentation } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';
import { wipe } from '@remotion/transitions/wipe';
import { Scene } from './Scene';
import { Captions } from './Captions';
import { StickmanDecorations } from './StickmanDecorations';
import { FPS } from './Root';
import type { VideoProps } from './types';

const TRANSITION_FRAMES = 10; // 10 frames (~0.33s) snappy stickman transitions

const PRESENTATIONS: Array<() => TransitionPresentation<any>> = [
  () => fade(),
  () => fade(),
  () => slide({ direction: 'from-right' }),
  () => fade(),
  () => wipe({ direction: 'from-left' }),
  () => fade(),
];

export const MainVideo: React.FC<VideoProps> = ({ timeline, captions }) => {
  if (!timeline || !timeline.scenes || timeline.scenes.length === 0) {
    return (
      <AbsoluteFill style={{ backgroundColor: '#FFF7E8', justifyContent: 'center', alignItems: 'center' }}>
        <h1 style={{ color: '#172A46', fontFamily: 'sans-serif' }}>Memuat data timeline...</h1>
      </AbsoluteFill>
    );
  }

  // Calculate cumulative scene boundary frames
  const boundaries = timeline.scenes.map((s) => Math.round((s.startMs / 1000) * FPS));
  const total = Math.round((timeline.audioDurationMs / 1000) * FPS);
  boundaries.push(total);

  const base = boundaries.slice(0, -1).map((b, i) => boundaries[i + 1] - b);

  // Transition duration per scene
  const tFrames = base.map((d, i) => {
    if (i === base.length - 1) return 0;
    return Math.max(0, Math.min(TRANSITION_FRAMES, Math.floor(d / 2), Math.floor(base[i + 1] / 2)));
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#FFF7E8' }}>
      {/* Background audio */}
      {timeline.audio && <Audio src={staticFile(timeline.audio)} />}

      {/* Visual scenes sequence */}
      <TransitionSeries>
        {timeline.scenes.flatMap((scene, i) => {
          const duration = base[i] + tFrames[i];
          const items = [
            <TransitionSeries.Sequence key={`s-${scene.id}`} durationInFrames={duration}>
              <Scene src={staticFile(scene.image)} index={i} durationInFrames={duration} />
            </TransitionSeries.Sequence>,
          ];

          if (tFrames[i] > 0) {
            items.push(
              <TransitionSeries.Transition
                key={`t-${scene.id}`}
                presentation={PRESENTATIONS[i % PRESENTATIONS.length]()}
                timing={linearTiming({ durationInFrames: tFrames[i] })}
              />
            );
          }
          return items;
        })}
      </TransitionSeries>

      {/* Persistent Stickman UI badges & stickers */}
      <StickmanDecorations />

      {/* Interactive Subtitles / Captions */}
      <Captions captions={captions} />
    </AbsoluteFill>
  );
};

