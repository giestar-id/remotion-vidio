import React from 'react';
import {
  DocumentaryMainVideo,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from '../Documentary';
import type {VideoProps} from '../types';

const PERSIA_CONFIG: DocumentaryHeaderConfig = {
  headerTitle: 'SEJARAH PERSIA',
  channelName: 'ZEELACUNA',
};

// Transisi wipe / slide halus hanya di pergantian babak sejarah besar, selain itu dominan fade tenang
const CHAPTER_WIPE_BEFORE_IDS = new Set([31, 66, 96, 146, 176]);
const CHAPTER_SLIDE_BEFORE_IDS = new Set([49, 79, 131, 191]);

// Marker era dinonaktifkan agar video bersih dari pop-up teks berulang
const ERA_MARKERS: EraMarker[] = [];

export const PersiaDocu: React.FC<VideoProps> = ({timeline, captions}) => {
  return (
    <DocumentaryMainVideo
      timeline={timeline}
      captions={captions}
      config={PERSIA_CONFIG}
      eraMarkers={ERA_MARKERS}
      chapterWipeIds={CHAPTER_WIPE_BEFORE_IDS}
      chapterSlideIds={CHAPTER_SLIDE_BEFORE_IDS}
    />
  );
};
