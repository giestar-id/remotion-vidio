import React, {useMemo} from 'react';
import {AbsoluteFill, Easing, Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {createTikTokStyleCaptions} from '@remotion/captions';
import type {Caption, TikTokPage} from '@remotion/captions';

const SWITCH_CAPTIONS_EVERY_MS = 1400;
const HIGHLIGHT_COLOR = '#D6A84F';
const BASE_COLOR = '#FFF5E6';
const PANEL_BG = 'rgba(36, 31, 26, 0.82)';
const PANEL_BORDER = '#8B5E3C';
const FONT_STACK = 'Georgia, "Times New Roman", serif';

const CaptionPage: React.FC<{page: TikTokPage}> = ({page}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const absoluteTimeMs = page.startMs + (frame / fps) * 1000;

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-end',
        alignItems: 'center',
        paddingBottom: '8%',
      }}
    >
      <div
        style={{
          maxWidth: '72%',
          padding: '22px 36px 24px',
          textAlign: 'center',
          backgroundColor: PANEL_BG,
          borderRadius: 12,
          borderTop: `2px solid ${PANEL_BORDER}`,
          boxShadow: '0 8px 28px rgba(0,0,0,0.35)',
        }}
      >
        <div
          style={{
            fontFamily: FONT_STACK,
            fontSize: 46,
            fontWeight: 600,
            lineHeight: 1.35,
            whiteSpace: 'pre-wrap',
            color: BASE_COLOR,
          }}
        >
          {page.tokens.map((token) => {
            const active = token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;
            return (
              <span
                key={token.fromMs}
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

export const SejarahCaptions: React.FC<{captions: Caption[]}> = ({captions}) => {
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
            <CaptionPage page={page} />
          </Sequence>
        );
      })}
    </>
  );
};

export const SejarahDecorations: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const intro = interpolate(frame, [0, fps * 0.8], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  const titleOut = interpolate(frame, [fps * 7, fps * 9], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {/* Tekstur: vignette ringan di tepi frame */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background:
            'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(20,15,8,0.42) 100%)',
          mixBlendMode: 'multiply',
        }}
      />
      {/* Garis bingkai tinta tipis */}
      <div
        style={{
          position: 'absolute',
          inset: 26,
          border: '1px solid rgba(139, 94, 60, 0.55)',
          borderRadius: 4,
        }}
      />

      {/* Pojok kiri atas: badge arsip */}
      <div
        style={{
          position: 'absolute',
          top: 44,
          left: 52,
          padding: '9px 16px',
          backgroundColor: 'rgba(244, 231, 207, 0.88)',
          border: '1px solid rgba(36, 31, 26, 0.45)',
          borderRadius: 4,
          fontFamily: 'Georgia, serif',
          fontSize: 17,
          letterSpacing: 4,
          fontWeight: 700,
          color: '#241F1A',
          opacity: intro,
        }}
      >
        DOKUMENTER SEJARAH
      </div>

      {/* Pojok kanan atas: pill */}
      <div
        style={{
          position: 'absolute',
          top: 44,
          right: 52,
          padding: '8px 16px',
          backgroundColor: 'rgba(36, 31, 26, 0.62)',
          border: '1px solid rgba(139, 94, 60, 0.9)',
          borderRadius: 999,
          fontFamily: 'Georgia, serif',
          fontSize: 15,
          letterSpacing: 3,
          fontWeight: 700,
          color: '#F4E7CF',
          opacity: 0.85 * intro,
        }}
      >
        FAKTA SEJARAH
      </div>

      {/* Judul pembuka (frame 0 sampai ±9 detik) */}
      <div
        style={{
          position: 'absolute',
          left: 90,
          right: '40%',
          top: '18%',
          opacity: intro * titleOut,
          transform: `translateY(${(1 - intro) * 24}px)`,
        }}
      >
        <div
          style={{
            borderBottom: '2px solid rgba(214, 168, 79, 0.9)',
            display: 'inline-block',
            paddingBottom: 10,
          }}
        >
          <div
            style={{
              fontFamily: 'Georgia, "Times New Roman", serif',
              fontSize: 86,
              fontWeight: 800,
              color: '#F4E7CF',
              textShadow: '0 3px 6px rgba(20,15,8,0.95), 0 3px 22px rgba(0,0,0,0.85)',
            }}
          >
            Perang Basus
          </div>
        </div>
        <div
          style={{
            marginTop: 14,
            fontFamily: 'Georgia, serif',
            fontSize: 28,
            letterSpacing: 2,
            color: '#D6A84F',
            textShadow: '0 2px 4px rgba(20,15,8,0.95), 0 2px 14px rgba(0,0,0,0.85)',
          }}
        >
          Ketika Seekor Unta Memecah Bangsa
        </div>
        <div
          style={{
            marginTop: 8,
            fontFamily: 'Georgia, serif',
            fontSize: 20,
            letterSpacing: 1,
            color: 'rgba(244, 231, 207, 0.95)',
            textShadow: '0 2px 4px rgba(20,15,8,0.95), 0 2px 14px rgba(0,0,0,0.85)',
          }}
        >
          Arabia pada Abad Ke-6 Masehi
        </div>
      </div>
    </AbsoluteFill>
  );
};
