import React from 'react';
import { Composition, staticFile } from 'remotion';
import type { Caption } from '@remotion/captions';
import { MainVideo } from './MainVideo';
import type { Timeline, VideoProps } from './types';
import { SejarahDocu } from './Sejarah';
import { YunaniDocu } from './Yunani';
import { SejarahIslamDocu } from './SejarahIslam';
import { ChinaDocu } from './China';
import { PiramidaMainVideo } from './StickmanPiramida';
import { RomaDocu } from './Roma';
import { PersiaDocu } from './Persia';
import { OrangIndoMainVideo } from './StickmanOrangIndo';
import { MajapahitDocu } from './Majapahit';
import { TajMahalMainVideo } from './StickmanTajMahal';
import { KulitMainVideo } from './StickmanKulit';
import { TakTidurMainVideo } from './StickmanTakTidur';

export const FPS = 30;

const createMetadataCalculator = () => async ({ props }: { props: VideoProps }) => {
  try {
    const timelineRes = await fetch(staticFile(`${props.proyek}/timeline.json`));
    const timeline: Timeline = await timelineRes.json();

    const captionsRes = await fetch(staticFile(`${props.proyek}/captions.json`));
    const captions: Caption[] = await captionsRes.json();

    const durationInFrames = Math.max(
      1,
      Math.round((timeline.audioDurationMs / 1000) * FPS)
    );

    return {
      durationInFrames,
      props: {
        ...props,
        timeline,
        captions,
      },
    };
  } catch (e) {
    console.error(`Error loading metadata for ${props.proyek} in Root:`, e);
    return {
      durationInFrames: FPS * 10,
      props,
    };
  }
};

export const Root: React.FC = () => {
  return (
    <>
      {/* V1 composition with visual2 */}
      <Composition
        id="MainVideo"
        component={MainVideo}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 10}
        defaultProps={
          {
            proyek: 'stickman',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      {/* V2 composition with visual2-2 */}
      <Composition
        id="MainVideoV2"
        component={MainVideo}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 10}
        defaultProps={
          {
            proyek: 'stickman2',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="SejarahDocu"
        component={SejarahDocu}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 10}
        defaultProps={
          {
            proyek: 'sejarah-1',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="SejarahYunani"
        component={YunaniDocu}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 10}
        defaultProps={
          {
            proyek: 'yunani',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="SejarahIslam"
        component={SejarahIslamDocu}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 10}
        defaultProps={
          {
            proyek: 'sejarah-2',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="SejarahChina"
        component={ChinaDocu}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 641}
        defaultProps={
          {
            proyek: 'china',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="PiramidaStickman"
        component={PiramidaMainVideo}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 500}
        defaultProps={
          {
            proyek: 'piramida',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="SejarahRoma"
        component={RomaDocu}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 819}
        defaultProps={
          {
            proyek: 'roma',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="SejarahPersia"
        component={PersiaDocu}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 777}
        defaultProps={
          {
            proyek: 'persia',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="OrangIndoPertama"
        component={OrangIndoMainVideo}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 308}
        defaultProps={
          {
            proyek: 'orang-indo-pertama',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="SejarahMajapahit"
        component={MajapahitDocu}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 632}
        defaultProps={
          {
            proyek: 'majapahit',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="TajMahalStickman"
        component={TajMahalMainVideo}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 385}
        defaultProps={
          {
            proyek: 'tajmahal',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="KulitStickman"
        component={KulitMainVideo}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 372}
        defaultProps={
          {
            proyek: 'kulit',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />

      <Composition
        id="TakTidurStickman"
        component={TakTidurMainVideo}
        width={1920}
        height={1080}
        fps={FPS}
        durationInFrames={FPS * 379}
        defaultProps={
          {
            proyek: 'tak-tidur',
            timeline: null,
            captions: [],
          } satisfies VideoProps
        }
        calculateMetadata={createMetadataCalculator()}
      />
    </>
  );
};


