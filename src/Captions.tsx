import React, { useMemo } from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from 'remotion';
import { createTikTokStyleCaptions } from '@remotion/captions';
import type { Caption, TikTokPage } from '@remotion/captions';

const SWITCH_CAPTIONS_EVERY_MS = 1400; // grouping window

const CaptionPage: React.FC<{ page: TikTokPage; from: number }> = ({ page, from }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // Exact audio synchronization by using current global frame
  const currentGlobalFrame = from + frame;
  const absoluteTimeMs = (currentGlobalFrame / fps) * 1000;

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-end',
        alignItems: 'center',
        paddingBottom: 75,
        pointerEvents: 'none',
        zIndex: 100,
      }}
    >
      <div
        style={{
          maxWidth: '82%',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '8px 12px',
          backgroundColor: '#FFF7E8',
          border: '3.5px solid #172A46',
          borderRadius: 22,
          padding: '16px 32px',
          boxShadow: '4px 4px 0px #172A46',
        }}
      >
        {page.tokens.map((token, i) => {
          const active = token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;
          const cleanText = token.text.trim();
          if (!cleanText) return null;

          return (
            <span
              key={`${token.fromMs}-${i}`}
              style={{
                fontSize: 34,
                fontWeight: 900,
                lineHeight: 1.25,
                fontFamily: 'system-ui, -apple-system, sans-serif',
                color: '#172A46',
                backgroundColor: active ? '#FFD34E' : 'transparent',
                border: active ? '2px solid #172A46' : '2px solid transparent',
                borderRadius: 10,
                padding: '2px 8px',
                transform: active ? 'scale(1.08)' : 'scale(1)',
                transition: 'all 0.08s ease-out',
                display: 'inline-block',
              }}
            >
              {cleanText}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const Captions: React.FC<{ captions: Caption[] }> = ({ captions }) => {
  const { fps } = useVideoConfig();
  const { pages } = useMemo(
    () =>
      createTikTokStyleCaptions({
        captions,
        combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS,
      }),
    [captions]
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

