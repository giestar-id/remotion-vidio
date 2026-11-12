import type {Caption} from '@remotion/captions';

export type TimelineScene = {
  id: number;
  startMs: number;
  endMs: number;
  image: string;
  matchRatio?: number;
  words?: number;
};

export type Timeline = {
  audioDurationMs: number;
  audio: string;
  scenes: TimelineScene[];
};

export type VideoProps = {
  proyek: string;
  timeline: Timeline | null;
  captions: Caption[];
};

