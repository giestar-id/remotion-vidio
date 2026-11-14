import React from 'react';
import {
  DocumentaryMainVideo,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from '../Documentary';
import type {VideoProps} from '../types';

const CHINA_CONFIG: DocumentaryHeaderConfig = {
  headerTitle: 'SEJARAH TEMBOK BESAR CHINA',
  channelName: 'SEJARAH CINA',
};

// Transisi wipe/slide hanya di pergantian babak dinasti besar, selain itu dominan fade tenang
const CHAPTER_WIPE_BEFORE_IDS = new Set([26, 78, 139, 176, 211, 243]);
const CHAPTER_SLIDE_BEFORE_IDS = new Set([42, 117, 159, 200, 221]);

// Marker era dinonaktifkan sesuai arahan pengguna agar video bersih tanpa pop-up teks berulang di bawah
const ERA_MARKERS: EraMarker[] = [];

export const ChinaDocu: React.FC<VideoProps> = ({timeline, captions}) => {
  return (
    <DocumentaryMainVideo
      timeline={timeline}
      captions={captions}
      config={CHINA_CONFIG}
      eraMarkers={ERA_MARKERS}
      chapterWipeIds={CHAPTER_WIPE_BEFORE_IDS}
      chapterSlideIds={CHAPTER_SLIDE_BEFORE_IDS}
    />
  );
};
