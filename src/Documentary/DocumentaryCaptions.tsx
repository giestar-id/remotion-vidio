import React, {useMemo} from 'react';
import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {createTikTokStyleCaptions} from '@remotion/captions';
import type {Caption, TikTokPage} from '@remotion/captions';

const SWITCH_CAPTIONS_EVERY_MS = 4000;
const HIGHLIGHT_COLOR = '#D6A84F';
const BASE_COLOR = '#FFF5E6';
const PANEL_BG = 'rgba(26, 22, 17, 0.84)';
const PANEL_BORDER_TOP = '#A93226';
const PANEL_BORDER_SUBTLE = 'rgba(139, 94, 60, 0.42)';
const SERIF_FONT = 'Georgia, "Palatino Linotype", "Times New Roman", serif';
const SANS_HEADER_FONT = '"Segoe UI", "Bahnschrift", system-ui, sans-serif';
const ACCENT_RED = '#A93226';
const CREAM_TEXT = '#F4E7CF';

export type DocumentaryHeaderConfig = {
  headerTitle: string;
  headerSubtitle?: string;
  channelName: string;
};

export type EraMarker = {
  id: string;
  startMs: number;
  endMs: number;
  dateLabel: string;
  titleLabel: string;
};

const CaptionPage: React.FC<{page: TikTokPage; from: number}> = ({page, from}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  // Gunakan frame global agar tidak ada sub-frame drift terhadap audio master
  const absoluteTimeMs = ((from + frame) / fps) * 1000;

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-end',
        alignItems: 'center',
        paddingBottom: 32,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          maxWidth: '74%',
          padding: '16px 34px 18px',
          textAlign: 'center',
          backgroundColor: PANEL_BG,
          borderRadius: 10,
          borderTop: `2px solid ${PANEL_BORDER_TOP}`,
          borderRight: `1px solid ${PANEL_BORDER_SUBTLE}`,
          borderBottom: `1px solid ${PANEL_BORDER_SUBTLE}`,
          borderLeft: `1px solid ${PANEL_BORDER_SUBTLE}`,
          boxShadow: '0 10px 30px rgba(0, 0, 0, 0.45)',
        }}
      >
        <div
          style={{
            fontFamily: SERIF_FONT,
            fontSize: 40,
            fontWeight: 600,
            lineHeight: 1.38,
            whiteSpace: 'pre-wrap',
            color: BASE_COLOR,
          }}
        >
          {page.tokens.map((token, idx) => {
            const active = token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;
            return (
              <span
                key={`${token.fromMs}-${idx}`}
                style={{
                  color: active ? HIGHLIGHT_COLOR : BASE_COLOR,
                  textDecoration: active ? 'underline' : 'none',
                  textUnderlineOffset: 6,
                  textDecorationThickness: 2,
                }}
              >
                {token.text}
              </span>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/**
 * Renders deterministic serif captions with gold word highlighting on dark charcoal panels.
 */
export const DocumentaryCaptions: React.FC<{captions: Caption[]}> = ({captions}) => {
  const {fps} = useVideoConfig();
  const {pages} = useMemo(
    () =>
      createTikTokStyleCaptions({
        captions,
        combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS,
      }),
    [captions],
  );

  return (
    <>
      {pages.map((page, index) => {
        const next = pages[index + 1] ?? null;
        const from = Math.round((page.startMs / 1000) * fps);
        const endMs = next ? next.startMs : page.startMs + SWITCH_CAPTIONS_EVERY_MS;
        const duration = Math.round(((endMs - page.startMs) / 1000) * fps);
        if (duration < 1) return null;
        return (
          <Sequence key={index} from={from} durationInFrames={duration}>
            <CaptionPage page={page} from={from} />
          </Sequence>
        );
      })}
    </>
  );
};

// Partikel debu arsip tipis deterministik (selaras atmosfer dokumenter di screenshot)
const DUST_PARTICLES = Array.from({length: 20}, (_, i) => ({
  x0: (i * 97 + 13) % 100,
  y0: (i * 53 + 29) % 100,
  vx: ((i % 5) - 2) * 0.012,
  vy: -0.018 - (i % 4) * 0.008,
  size: 2 + (i % 3) * 1.4,
  dark: i % 3 === 0,
  baseOpacity: 0.14 + (i % 4) * 0.05,
}));

/**
 * Renders documentary atmosphere (vignette, top gradient scrim, dust motes)
 * and corner channel branding.
 */
export const DocumentaryDecorations: React.FC<{config: DocumentaryHeaderConfig}> = ({config}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const headerOpacity = interpolate(frame, [0, fps * 0.7], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {/* Vignette ringan di tepi frame */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background:
            'radial-gradient(ellipse at center, rgba(0,0,0,0) 56%, rgba(18,14,9,0.44) 100%)',
          mixBlendMode: 'multiply',
        }}
      />

      {/* Scrim gradasi lembut di sisi atas agar teks header tetap tajam */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 150,
          background:
            'linear-gradient(180deg, rgba(16, 13, 9, 0.58) 0%, rgba(16, 13, 9, 0.22) 55%, rgba(16, 13, 9, 0) 100%)',
        }}
      />

      {/* Partikel debu arsip tipis & tenang */}
      {DUST_PARTICLES.map((p, idx) => {
        const px = (p.x0 + frame * p.vx + 100) % 100;
        const py = ((p.y0 + frame * p.vy) % 100 + 100) % 100;
        return (
          <div
            key={idx}
            style={{
              position: 'absolute',
              left: `${px}%`,
              top: `${py}%`,
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              backgroundColor: p.dark ? 'rgba(36, 31, 26, 0.35)' : 'rgba(244, 231, 207, 0.45)',
              opacity: p.baseOpacity,
            }}
          />
        );
      })}

      {/* POJOK KIRI ATAS: Garis vertikal merah tua + judul utama (+ subjudul opsional) */}
      <div
        style={{
          position: 'absolute',
          top: config.headerSubtitle ? 38 : 40,
          left: 48,
          display: 'flex',
          alignItems: 'center',
          gap: 14,
          opacity: headerOpacity,
        }}
      >
        <div
          style={{
            width: 5,
            height: config.headerSubtitle ? 44 : 26,
            backgroundColor: ACCENT_RED,
            borderRadius: 1,
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.6)',
          }}
        />
        <div style={{display: 'flex', flexDirection: 'column', gap: 3}}>
          <div
            style={{
              fontFamily: SANS_HEADER_FONT,
              fontSize: 22,
              fontWeight: 700,
              letterSpacing: 4.5,
              lineHeight: 1.1,
              color: CREAM_TEXT,
              textShadow: '0 2px 10px rgba(10, 8, 5, 0.88)',
            }}
          >
            {config.headerTitle}
          </div>
          {config.headerSubtitle && (
            <div
              style={{
                fontFamily: SANS_HEADER_FONT,
                fontSize: 12,
                fontWeight: 500,
                letterSpacing: 2.8,
                lineHeight: 1.1,
                color: 'rgba(244, 231, 207, 0.74)',
                textShadow: '0 1px 6px rgba(10, 8, 5, 0.88)',
              }}
            >
              {config.headerSubtitle}
            </div>
          )}
        </div>
      </div>

      {/* POJOK KANAN ATAS: Nama channel dengan style tipografi arsip bersih */}
      <div
        style={{
          position: 'absolute',
          top: 44,
          right: 52,
          fontFamily: SANS_HEADER_FONT,
          fontSize: 15,
          fontWeight: 600,
          letterSpacing: 4.5,
          color: 'rgba(244, 231, 207, 0.84)',
          textShadow: '0 2px 8px rgba(10, 8, 5, 0.88)',
          opacity: headerOpacity,
        }}
      >
        {config.channelName}
      </div>
    </AbsoluteFill>
  );
};

/**
 * Renders transient chronological milestone lower-thirds above the subtitle band.
 */
export const EraLowerThirds: React.FC<{markers: EraMarker[]}> = ({markers}) => {
  const {fps} = useVideoConfig();

  return (
    <>
      {markers.map((m) => {
        const from = Math.round((m.startMs / 1000) * fps);
        const duration = Math.round(((m.endMs - m.startMs) / 1000) * fps);
        if (duration < 10) return null;
        return (
          <Sequence key={m.id} from={from} durationInFrames={duration}>
            <EraLowerThirdCard dateLabel={m.dateLabel} titleLabel={m.titleLabel} duration={duration} />
          </Sequence>
        );
      })}
    </>
  );
};

const EraLowerThirdCard: React.FC<{
  dateLabel: string;
  titleLabel: string;
  duration: number;
}> = ({dateLabel, titleLabel, duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const fadeIn = interpolate(frame, [0, Math.round(fps * 0.45)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const fadeOut = interpolate(frame, [duration - Math.round(fps * 0.55), duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const alpha = fadeIn * fadeOut;

  return (
    <div
      style={{
        position: 'absolute',
        left: 48,
        bottom: 204,
        padding: '10px 18px',
        backgroundColor: 'rgba(26, 22, 17, 0.78)',
        borderLeft: `3px solid ${HIGHLIGHT_COLOR}`,
        borderRadius: '0 6px 6px 0',
        boxShadow: '0 6px 20px rgba(0,0,0,0.35)',
        opacity: alpha,
        transform: `translateX(${(1 - fadeIn) * -14}px)`,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          fontFamily: SANS_HEADER_FONT,
          fontSize: 12,
          fontWeight: 700,
          letterSpacing: 3,
          color: HIGHLIGHT_COLOR,
        }}
      >
        {dateLabel}
      </div>
      <div
        style={{
          marginTop: 2,
          fontFamily: SERIF_FONT,
          fontSize: 20,
          fontWeight: 600,
          color: CREAM_TEXT,
        }}
      >
        {titleLabel}
      </div>
    </div>
  );
};
