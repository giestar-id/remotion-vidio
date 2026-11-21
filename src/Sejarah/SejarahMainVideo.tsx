import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import type {Caption} from '@remotion/captions';
import {SejarahScene} from './SejarahScene';
import {SejarahCaptions, SejarahDecorations} from './SejarahCaptions';
import {FPS} from '../Root';
import type {Timeline} from '../types';

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

  const base = boundaries.slice(0, -1).map((b, i) => Math.max(1, boundaries[i + 1] - b));

  return (
    <AbsoluteFill style={{backgroundColor: BASE_BG}}>
      {timeline.audio && <Audio src={staticFile(timeline.audio)} />}

      {/* Visual scenes sequence - 100% Hard-cut murni */}
      {timeline.scenes.map((scene, i) => {
        const from = boundaries[i];
        const duration = base[i];
        return (
          <Sequence key={`s-${scene.id}`} from={from} durationInFrames={duration}>
            <SejarahScene
              src={staticFile(scene.image)}
              index={i}
              durationInFrames={duration}
            />
          </Sequence>
        );
      })}

      <SejarahDecorations />
      <SejarahCaptions captions={captions} />
    </AbsoluteFill>
  );
};
