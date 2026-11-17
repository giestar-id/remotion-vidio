import React from 'react';
import {
  DocumentaryMainVideo,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from '../Documentary';
import type {VideoProps} from '../types';

const MAJAPAHIT_CONFIG: DocumentaryHeaderConfig = {
  headerTitle: 'SEJARAH MAJAPAHIT',
  channelName: 'ZEELACUNA',
};

// Transisi wipe / slide halus di pergantian babak penting
const CHAPTER_WIPE_BEFORE_IDS = new Set([25, 55, 85, 115]);
const CHAPTER_SLIDE_BEFORE_IDS = new Set([40, 70, 100, 130]);

// Marker era dinonaktifkan agar video bersih dari pop-up teks berulang
const ERA_MARKERS: EraMarker[] = [];

export const MajapahitDocu: React.FC<VideoProps> = ({timeline, captions}) => {
  return (
    <DocumentaryMainVideo
      timeline={timeline}
      captions={captions}
      config={MAJAPAHIT_CONFIG}
      eraMarkers={ERA_MARKERS}
      chapterWipeIds={CHAPTER_WIPE_BEFORE_IDS}
      chapterSlideIds={CHAPTER_SLIDE_BEFORE_IDS}
    />
  );
};
