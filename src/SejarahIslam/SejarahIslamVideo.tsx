import React from 'react';
import {
  DocumentaryMainVideo,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from '../Documentary';
import type {VideoProps} from '../types';

const SEJARAH_ISLAM_CONFIG: DocumentaryHeaderConfig = {
  headerTitle: 'SEJARAH ISLAM',
  channelName: 'SEJARAONE',
};

const CHAPTER_WIPE_BEFORE_IDS = new Set([16, 34, 70, 105, 134, 173]);
const CHAPTER_SLIDE_BEFORE_IDS = new Set([26, 55, 89, 118, 149, 195]);

const ERA_MARKERS: EraMarker[] = [
  {
    id: 'makkah',
    startMs: 63200,
    endMs: 67800,
    dateLabel: '610 M · MAKKAH AL-MUKARRAMAH',
    titleLabel: 'Masyarakat Quraisy & Zaman Jahiliyah',
  },
  {
    id: 'darul-arqam',
    startMs: 103500,
    endMs: 108200,
    dateLabel: 'FASE AWAL · DARUL ARQAM',
    titleLabel: 'Dakwah Sembunyi-sembunyi (± 3 Tahun)',
  },
  {
    id: 'bukit-safa',
    startMs: 138600,
    endMs: 143200,
    dateLabel: 'DAKWAH TERBUKA · BUKIT SAFA',
    titleLabel: 'Seruan Kebenaran & Reaksi Elit Quraisy',
  },
  {
    id: 'habasyah',
    startMs: 246300,
    endMs: 251000,
    dateLabel: 'SUAKA LINTAS BENUA · AXUM',
    titleLabel: 'Hijrah ke Negeri Habasyah (Raja Najasyi)',
  },
  {
    id: 'boikot',
    startMs: 280500,
    endMs: 285200,
    dateLabel: "SYI'B ABI THALIB · ± 3 TAHUN",
    titleLabel: 'Boikot Ekonomi & Sosial Bani Hasyim',
  },
  {
    id: 'amul-huzni',
    startMs: 331800,
    endMs: 336500,
    dateLabel: 'TAHUN DUKA CITA · AMUL HUZNI',
    titleLabel: 'Wafatnya Abu Thalib & Khadijah r.a.',
  },
  {
    id: 'aqabah',
    startMs: 430700,
    endMs: 435400,
    dateLabel: 'PERJANJIAN AQABAH · YATSRIB',
    titleLabel: "Bai'at Aqabah & Jalan Menuju Madinah",
  },
  {
    id: 'hijrah',
    startMs: 550500,
    endMs: 555300,
    dateLabel: '622 M · MADINATUN NABI',
    titleLabel: 'Peristiwa Hijrah & Kelahiran Tamaddun',
  },
  {
    id: 'pilar-madinah',
    startMs: 623100,
    endMs: 627800,
    dateLabel: 'KOTA MADINAH · TIGA PILAR',
    titleLabel: "Masjid Nabawi, Al-Mu'akhah & Piagam Madinah",
  },
  {
    id: 'piagam-madinah',
    startMs: 729500,
    endMs: 734200,
    dateLabel: 'KONSTITUSI MADINAH · UMMAH',
    titleLabel: 'Perjanjian Tertulis Masyarakat Majemuk',
  },
];

/**
 * Documentary composition for the 15-minute History of Islam narrative.
 */
export const SejarahIslamDocu: React.FC<VideoProps> = ({timeline, captions}) => {
  return (
    <DocumentaryMainVideo
      timeline={timeline}
      captions={captions}
      config={SEJARAH_ISLAM_CONFIG}
      eraMarkers={ERA_MARKERS}
      chapterWipeIds={CHAPTER_WIPE_BEFORE_IDS}
      chapterSlideIds={CHAPTER_SLIDE_BEFORE_IDS}
      sceneBaseScaleOffset={0.065}
    />
  );
};

