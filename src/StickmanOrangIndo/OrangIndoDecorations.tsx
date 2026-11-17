import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const OrangIndoDecorations: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance spring animation for badges
  const badgeEntrance = spring({
    frame,
    fps,
    config: {
      damping: 12,
      stiffness: 100,
      mass: 0.8,
    },
  });

  const badgeScale = interpolate(badgeEntrance, [0, 1], [0.8, 1]);
  const badgeOpacity = interpolate(badgeEntrance, [0, 1], [0, 1]);

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {/* Top Left Pill: OTAK ATIK */}
      <div
        style={{
          position: 'absolute',
          top: 40,
          left: 50,
          display: 'flex',
          alignItems: 'center',
          backgroundColor: '#FFD34E',
          border: '3.5px solid #172A46',
          borderRadius: 999,
          padding: '10px 28px',
          boxShadow: '4px 4px 0px #172A46',
          transform: `scale(${badgeScale}) rotate(-1.2deg)`,
          opacity: badgeOpacity,
          zIndex: 50,
        }}
      >
        <span
          style={{
            fontSize: 16,
            fontWeight: 900,
            letterSpacing: 2,
            color: '#172A46',
            fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            textTransform: 'uppercase',
          }}
        >
          OTAK ATIK
        </span>
      </div>
    </AbsoluteFill>
  );
};
