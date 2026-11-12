import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const StickmanDecorations: React.FC = () => {
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
      {/* Top Left Badge: PENGETAHUAN / KISAH EDISON */}
      <div
        style={{
          position: 'absolute',
          top: 40,
          left: 50,
          display: 'flex',
          alignItems: 'center',
          gap: 14,
          backgroundColor: '#FFF7E8',
          border: '3.5px solid #172A46',
          borderRadius: 18,
          padding: '10px 22px',
          boxShadow: '4px 4px 0px #172A46',
          transform: `scale(${badgeScale}) rotate(-1.5deg)`,
          opacity: badgeOpacity,
          zIndex: 50,
        }}
      >
        {/* Doodle Idea Lightbulb Icon */}
        <div
          style={{
            width: 38,
            height: 38,
            backgroundColor: '#FFD34E',
            border: '2.5px solid #172A46',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 20,
          }}
        >
          💡
        </div>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span
            style={{
              fontSize: 14,
              fontWeight: 900,
              letterSpacing: 1.5,
              color: '#F47C67',
              textTransform: 'uppercase',
              fontFamily: 'system-ui, -apple-system, sans-serif',
            }}
          >
            PENGETAHUAN STICKMAN
          </span>
          <span
            style={{
              fontSize: 20,
              fontWeight: 800,
              color: '#172A46',
              letterSpacing: 0.5,
              fontFamily: 'system-ui, -apple-system, sans-serif',
            }}
          >
            REKAMAN SUARA EDISON
          </span>
        </div>
      </div>

      {/* Top Right Pill: TAHUKAH KAMU? / FAKTA SEJARAH */}
      <div
        style={{
          position: 'absolute',
          top: 40,
          right: 50,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          backgroundColor: '#FFD34E',
          border: '3.5px solid #172A46',
          borderRadius: 999,
          padding: '10px 26px',
          boxShadow: '4px 4px 0px #172A46',
          transform: `scale(${badgeScale}) rotate(1.2deg)`,
          opacity: badgeOpacity,
          zIndex: 50,
        }}
      >
        <span
          style={{
            fontSize: 18,
            fontWeight: 900,
            color: '#172A46',
            letterSpacing: 1,
            textTransform: 'uppercase',
            fontFamily: 'system-ui, -apple-system, sans-serif',
          }}
        >
          ⭐ OTAK ATIK
        </span>
      </div>
    </AbsoluteFill>
  );
};

