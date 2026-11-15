import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const PiramidaDecorations: React.FC = () => {
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
      {/* Top Left Pill: OTAK OTIK */}
      <div
        style={{
          position: 'absolute',
          top: 40,
          left: 50,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          backgroundColor: '#FFD34E',
          border: '3.5px solid #172A46',
          borderRadius: 999,
          padding: '10px 24px',
          boxShadow: '4px 4px 0px #172A46',
          transform: `scale(${badgeScale}) rotate(-1.2deg)`,
          opacity: badgeOpacity,
          zIndex: 50,
        }}
      >
        <span style={{ fontSize: 16 }}>💡</span>
        <span
          style={{
            fontSize: 15,
            fontWeight: 800,
            letterSpacing: 1,
            color: '#172A46',
            fontFamily: 'system-ui, -apple-system, sans-serif',
          }}
        >
          OTAK OTIK
        </span>
      </div>
    </AbsoluteFill>
  );
};
