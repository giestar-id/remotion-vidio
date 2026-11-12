import React from 'react';
import { AbsoluteFill, Img, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

// Smooth, subtle stickman camera motions
const MOTIONS = [
  { from: { s: 1.0, x: 0, y: 0 }, to: { s: 1.035, x: 0, y: 0 } }, // gentle zoom in
  { from: { s: 1.035, x: 0, y: 0 }, to: { s: 1.0, x: 0, y: 0 } }, // gentle zoom out
  { from: { s: 1.025, x: -1.2, y: 0 }, to: { s: 1.025, x: 1.2, y: 0 } }, // slight pan left -> right
  { from: { s: 1.025, x: 1.2, y: 0 }, to: { s: 1.025, x: -1.2, y: 0 } }, // slight pan right -> left
];

export const Scene: React.FC<{
  src: string;
  index: number;
  durationInFrames: number;
}> = ({ src, index, durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Gentle pop-in bounce on scene transition
  const entryBounce = spring({
    frame,
    fps,
    config: {
      damping: 18,
      stiffness: 140,
      mass: 0.9,
    },
  });

  const m = MOTIONS[index % MOTIONS.length];
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // Base motion interpolation
  const s = m.from.s + (m.to.s - m.from.s) * p;
  const x = m.from.x + (m.to.x - m.from.x) * p;
  const y = m.from.y + (m.to.y - m.from.y) * p;

  // Multiply by entry bounce slightly (starts from 0.985 -> 1.0)
  const bounceScale = interpolate(entryBounce, [0, 1], [0.985, 1]);

  return (
    <AbsoluteFill style={{ overflow: 'hidden', backgroundColor: '#FFF7E8' }}>
      <Img
        src={src}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover', // fills 1920x1080 cleanly
          transform: `translate(${x}%, ${y}%) scale(${s * bounceScale})`,
        }}
      />
    </AbsoluteFill>
  );
};

