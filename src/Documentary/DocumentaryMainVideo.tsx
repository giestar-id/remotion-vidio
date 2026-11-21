import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import type {Caption} from '@remotion/captions';
import type {Timeline} from '../types';
import {DocumentaryScene} from './DocumentaryScene';
import {
  DocumentaryCaptions,
  DocumentaryDecorations,
  EraLowerThirds,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from './DocumentaryCaptions';

const BASE_BG = '#241F1A';

export type DocumentaryMainVideoProps = {
  timeline: Timeline | null;
  captions: Caption[];
  config: DocumentaryHeaderConfig;
  eraMarkers: EraMarker[];
  chapterWipeIds: Set<number>;
  chapterSlideIds: Set<number>;
  sceneBaseScaleOffset?: number;
};

/**
 * Shared documentary timeline renderer: 100% hard-cut murni (tanpa transisi antar scene).
 */
export const DocumentaryMainVideo: React.FC<DocumentaryMainVideoProps> = ({
  timeline,
  captions,
  config,
  eraMarkers,
  sceneBaseScaleOffset = 0,
}) => {
  const {fps} = useVideoConfig();
  if (!timeline) return null;

  // Batas scene dalam frame kumulatif (dibulatkan sekali untuk mencegah akumulasi drift)
  const boundaries = timeline.scenes.map((s) => Math.round((s.startMs / 1000) * fps));
  const total = Math.round((timeline.audioDurationMs / 1000) * fps);
  boundaries.push(total);

  const base = boundaries.slice(0, -1).map((b, i) => Math.max(1, boundaries[i + 1] - b));

  return (
    <AbsoluteFill style={{backgroundColor: BASE_BG}}>
      {/* Background audio */}
      {timeline.audio && <Audio src={staticFile(timeline.audio)} />}

      {/* Visual scenes sequence - 100% Hard-cut murni tanpa transisi */}
      {timeline.scenes.map((scene, i) => {
        const from = boundaries[i];
        const duration = base[i];
        return (
          <Sequence key={`s-${scene.id}`} from={from} durationInFrames={duration}>
            <DocumentaryScene
              src={staticFile(scene.image)}
              index={i}
              durationInFrames={duration}
              baseScaleOffset={sceneBaseScaleOffset}
            />
          </Sequence>
        );
      })}

      {/* Header and Branding (tanpa badge era jika dinonaktifkan) */}
      <DocumentaryDecorations config={config} />

      {/* Optional era markers */}
      {eraMarkers && eraMarkers.length > 0 && <EraLowerThirds markers={eraMarkers} />}

      {/* Subtitles / Captions */}
      <DocumentaryCaptions captions={captions} />
    </AbsoluteFill>
  );
};
