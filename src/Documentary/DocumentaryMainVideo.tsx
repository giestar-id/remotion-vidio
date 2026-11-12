import React from 'react';
import {AbsoluteFill, Audio, staticFile, useVideoConfig} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import type {TransitionPresentation} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
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

const TRANSITION_FRAMES = 15; // 0.5s calm documentary transition at 30 fps
const BASE_BG = '#241F1A';

const getTransitionPresentation = (
  nextSceneId: number,
  wipeIds: Set<number>,
  slideIds: Set<number>,
): TransitionPresentation<any> => {
  if (wipeIds.has(nextSceneId)) {
    return wipe({direction: 'from-left'});
  }
  if (slideIds.has(nextSceneId)) {
    return slide({direction: 'from-right'});
  }
  return fade();
};

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
 * Shared documentary timeline renderer combining archival scenes, calm
 * transitions, era lower-thirds, serif captions, and corner branding.
 */
export const DocumentaryMainVideo: React.FC<DocumentaryMainVideoProps> = ({
  timeline,
  captions,
  config,
  eraMarkers,
  chapterWipeIds,
  chapterSlideIds,
  sceneBaseScaleOffset = 0,
}) => {
  const {fps} = useVideoConfig();
  if (!timeline) return null;

  // Batas scene dalam frame kumulatif (dibulatkan sekali untuk mencegah akumulasi drift)
  const boundaries = timeline.scenes.map((s) => Math.round((s.startMs / 1000) * fps));
  const total = Math.round((timeline.audioDurationMs / 1000) * fps);
  boundaries.push(total);

  const base = boundaries.slice(0, -1).map((b, i) => boundaries[i + 1] - b);

  const tFrames = base.map((d, i) => {
    if (i === base.length - 1) return 0;
    return Math.max(0, Math.min(TRANSITION_FRAMES, Math.floor(d / 2), Math.floor(base[i + 1] / 2)));
  });

  return (
    <AbsoluteFill style={{backgroundColor: BASE_BG}}>
      <Audio src={staticFile(timeline.audio)} />

      <TransitionSeries>
        {timeline.scenes.flatMap((scene, i) => {
          const duration = base[i] + tFrames[i];
          const nextScene = timeline.scenes[i + 1];
          const items = [
            <TransitionSeries.Sequence key={`s-${scene.id}`} durationInFrames={duration}>
              <DocumentaryScene
                src={staticFile(scene.image)}
                index={i}
                durationInFrames={duration}
                baseScaleOffset={sceneBaseScaleOffset}
              />
            </TransitionSeries.Sequence>,
          ];
          if (tFrames[i] > 0 && nextScene) {
            items.push(
              <TransitionSeries.Transition
                key={`t-${scene.id}`}
                presentation={getTransitionPresentation(
                  nextScene.id,
                  chapterWipeIds,
                  chapterSlideIds,
                )}
                timing={linearTiming({durationInFrames: tFrames[i]})}
              />,
            );
          }
          return items;
        })}
      </TransitionSeries>

      <EraLowerThirds markers={eraMarkers} />
      <DocumentaryCaptions captions={captions} />
      <DocumentaryDecorations config={config} />
    </AbsoluteFill>
  );
};

