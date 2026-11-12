import React from 'react';
import {
  DocumentaryMainVideo,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from '../Documentary';
import type {VideoProps} from '../types';

const YUNANI_CONFIG: DocumentaryHeaderConfig = {
  headerTitle: 'SEJARAH YUNANI',
  channelName: 'SEJARAONE',
};

// Pergantian bab besar memakai wipe/slide halus; selain itu dominan fade (sesuai video-style-sejarah)
const CHAPTER_WIPE_BEFORE_IDS = new Set([14, 32, 72, 92, 131, 153]);
const CHAPTER_SLIDE_BEFORE_IDS = new Set([22, 45, 77, 108, 116, 149]);

// Penanda babak sejarah (lower-third singkat non-intrusif pada titik balik zaman)
const ERA_MARKERS: EraMarker[] = [
  {id: 'polis', startMs: 64730, endMs: 69000, dateLabel: 'ZAMAN ARKAIS · LAUT AEGEA', titleLabel: 'Terbentuknya Negara-Kota (Polis)'},
  {id: 'solon', startMs: 100920, endMs: 105400, dateLabel: '594 SM · ATHENA', titleLabel: 'Krisis Utang & Reformasi Hukum Solon'},
  {id: 'cleisthenes', startMs: 154350, endMs: 158900, dateLabel: '508 SM · ATHENA', titleLabel: 'Cleisthenes & Lahirnya Isonomia'},
  {id: 'persia', startMs: 223700, endMs: 228500, dateLabel: '490–479 SM · MARATHON — SALAMIS', titleLabel: 'Invasi Kekaisaran Persia'},
  {id: 'sparta', startMs: 375960, endMs: 380600, dateLabel: 'SPARTA · LEMBAH EUROTAS', titleLabel: 'Ilusi Sparta & Krisis Oliganthropia'},
  {id: 'peloponnesos', startMs: 447040, endMs: 451800, dateLabel: '431–404 SM · YUNANI', titleLabel: 'Perang Saudara Peloponnesos'},
  {id: 'makedonia', startMs: 531670, endMs: 536500, dateLabel: '338–323 SM · MAKEDONIA — ASIA', titleLabel: 'Philip II & Ekspedisi Alexander Agung'},
  {id: 'helenistik', startMs: 645380, endMs: 650100, dateLabel: 'ERA HELENISTIK · 323–146 SM', titleLabel: 'Aleksandria hingga Ai Khanoum'},
  {id: 'romawi', startMs: 731190, endMs: 736000, dateLabel: 'ABAD KE-2 SM · ROMAWI — KINI', titleLabel: 'Penaklukan Fisik & Warisan Pemikiran'},
];

export const YunaniDocu: React.FC<VideoProps> = ({timeline, captions}) => {
  return (
    <DocumentaryMainVideo
      timeline={timeline}
      captions={captions}
      config={YUNANI_CONFIG}
      eraMarkers={ERA_MARKERS}
      chapterWipeIds={CHAPTER_WIPE_BEFORE_IDS}
      chapterSlideIds={CHAPTER_SLIDE_BEFORE_IDS}
    />
  );
};
