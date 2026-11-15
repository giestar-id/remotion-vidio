import React from 'react';
import {
  DocumentaryMainVideo,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from '../Documentary';
import type {VideoProps} from '../types';

const ROMA_CONFIG: DocumentaryHeaderConfig = {
  headerTitle: 'SEJARAH ROMA',
  channelName: 'ZEELACUNA',
};

// Transisi wipe / slide halus hanya di pergantian babak besar, selain itu dominan fade tenang
const CHAPTER_WIPE_BEFORE_IDS = new Set([32, 96, 140, 195, 245]);
const CHAPTER_SLIDE_BEFORE_IDS = new Set([66, 120, 175, 218]);

// Marker era dinonaktifkan agar video bersih dari pop-up teks berulang
const ERA_MARKERS: EraMarker[] = [];

export const RomaDocu: React.FC<VideoProps> = ({timeline, captions}) => {
  return (
    <DocumentaryMainVideo
      timeline={timeline}
      captions={captions}
      config={ROMA_CONFIG}
      eraMarkers={ERA_MARKERS}
      chapterWipeIds={CHAPTER_WIPE_BEFORE_IDS}
      chapterSlideIds={CHAPTER_SLIDE_BEFORE_IDS}
    />
  );
};
