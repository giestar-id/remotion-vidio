import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { Scene } from '../Scene';
import { Captions } from '../Captions';
import { OrangIndoDecorations } from './OrangIndoDecorations';
import { FPS } from '../Root';
import type { VideoProps } from '../types';

export const OrangIndoMainVideo: React.FC<VideoProps> = ({ timeline, captions }) => {
  if (!timeline || !timeline.scenes || timeline.scenes.length === 0) {
    return (
      <AbsoluteFill style={{ backgroundColor: '#FFF7E8', justifyContent: 'center', alignItems: 'center' }}>
        <h1 style={{ color: '#172A46', fontFamily: 'sans-serif' }}>Memuat data timeline...</h1>
      </AbsoluteFill>
    );
  }

  // Calculate cumulative scene boundary frames (hard cut, tanpa transisi)
  const boundaries = timeline.scenes.map((s) => Math.round((s.startMs / 1000) * FPS));
  const total = Math.round((timeline.audioDurationMs / 1000) * FPS);
  boundaries.push(total);

  const base = boundaries.slice(0, -1).map((b, i) => Math.max(1, boundaries[i + 1] - b));

  return (
    <AbsoluteFill style={{ backgroundColor: '#FFF7E8' }}>
      {/* Background audio */}
      {timeline.audio && <Audio src={staticFile(timeline.audio)} />}

      {/* Visual scenes sequence - Hard cut instan tanpa transisi */}
      {timeline.scenes.map((scene, i) => {
        const from = boundaries[i];
        const duration = base[i];
        return (
          <Sequence key={`s-${scene.id}`} from={from} durationInFrames={duration}>
            <Scene src={staticFile(scene.image)} index={i} durationInFrames={duration} />
          </Sequence>
        );
      })}

      {/* Persistent Stickman UI badges */}
      <OrangIndoDecorations />

      {/* Interactive Subtitles / Captions */}
      <Captions captions={captions} />
    </AbsoluteFill>
  );
};
