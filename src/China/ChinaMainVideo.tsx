import React from 'react';
import {
  DocumentaryMainVideo,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from '../Documentary';
import type {VideoProps} from '../types';

const CHINA_CONFIG: DocumentaryHeaderConfig = {
  headerTitle: 'SEJARAH TEMBOK BESAR CHINA',
  channelName: 'SEJARAONE',
};

// Transisi wipe/slide hanya di pergantian babak dinasti besar, selain itu dominan fade tenang
const CHAPTER_WIPE_BEFORE_IDS = new Set([14, 39, 65, 85, 105, 125, 145]);
const CHAPTER_SLIDE_BEFORE_IDS = new Set([20, 52, 95, 115, 138]);

// Penanda babak sejarah sepanjang 10 menit dokumenter (lower-third elegan di atas subtitle)
const ERA_MARKERS: EraMarker[] = [
  {
    id: 'huanghe',
    startMs: 2500,
    endMs: 8000,
    dateLabel: 'PERADABAN LEMBAH SUNGAI KUNING',
    titleLabel: 'Lumpur Aluvial & Awal Agrikultur Kuno',
  },
  {
    id: 'hangtu',
    startMs: 11000,
    endMs: 16500,
    dateLabel: 'TEKNIK HANGTU · BENTENG TANAH LIAT',
    titleLabel: 'Perlindungan dari Banjir Bandang & Serangan',
  },
  {
    id: 'shang',
    startMs: 44000,
    endMs: 49500,
    dateLabel: '~1600 SM · DINASTI SHANG',
    titleLabel: 'Ibu Kota Anyang & Ritual Tulang Ramalan',
  },
  {
    id: 'tianming',
    startMs: 87000,
    endMs: 92500,
    dateLabel: '1046 SM · MANDAT LANGIT (TIANMING)',
    titleLabel: 'Kekuasaan Bersyarat & Keadilan Rakyat',
  },
  {
    id: 'mencius',
    startMs: 124000,
    endMs: 129500,
    dateLabel: 'ABAD KE-4 SM · PEMIKIR MENCIUS',
    titleLabel: 'Rakyat Nomor Satu, Penguasa Terbawah',
  },
  {
    id: 'qin',
    startMs: 147500,
    endMs: 153500,
    dateLabel: '221 SM · QIN SHI HUANG',
    titleLabel: 'Kekaisaran Tunggal & Tembok Besar Pertama',
  },
  {
    id: 'han',
    startMs: 215000,
    endMs: 221000,
    dateLabel: '202 SM–220 M · DINASTI HAN',
    titleLabel: 'Kertas Cai Lun & Pembukaan Jalur Sutra',
  },
  {
    id: 'tang',
    startMs: 285000,
    endMs: 291000,
    dateLabel: '618–907 M · KEEMASAN DINASTI TANG',
    titleLabel: 'Ibu Kota Chang\'an & Titik Temu Dunia',
  },
  {
    id: 'song',
    startMs: 322000,
    endMs: 328000,
    dateLabel: '960–1279 M · DINASTI SONG',
    titleLabel: 'Uang Kertas Jiaozi, Kompas & Mesiu',
  },
  {
    id: 'yuan',
    startMs: 385000,
    endMs: 391000,
    dateLabel: '1271–1368 M · DINASTI YUAN (MONGOL)',
    titleLabel: 'Kublai Khan & Penyatuan Jalur Darat Eurasia',
  },
  {
    id: 'ming',
    startMs: 440000,
    endMs: 446000,
    dateLabel: '1368–1644 M · DINASTI MING',
    titleLabel: 'Kota Terlarang, Ekspedisi Laut & Tembok Batu Bata',
  },
  {
    id: 'qing',
    startMs: 490000,
    endMs: 496000,
    dateLabel: '1644–1912 M · DINASTI QING',
    titleLabel: 'Era Keemasan Kangxi & Batas Wilayah Terluas',
  },
  {
    id: 'republik',
    startMs: 535000,
    endMs: 541000,
    dateLabel: '1911–1945 · ERA REPUBLIK',
    titleLabel: 'Sun Yat-sen & Ujian Perang Terberat',
  },
  {
    id: 'modern',
    startMs: 580000,
    endMs: 586500,
    dateLabel: '1949 — KINI · TIONGKOK MODERN',
    titleLabel: 'Warisan Ribuan Tahun dalam Negeri Modern',
  },
];

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
