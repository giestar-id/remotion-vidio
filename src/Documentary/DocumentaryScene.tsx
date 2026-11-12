import React from 'react';
import {AbsoluteFill, Img, interpolate, useCurrentFrame} from 'remotion';

// Ken Burns sangat tenang dan lembut (skala <= 5.5%, pan halus bergantian)
const MOTIONS = [
  {from: {s: 1.0, x: 0, y: 0}, to: {s: 1.055, x: 0, y: 0}}, // zoom in
  {from: {s: 1.055, x: 0, y: 0}, to: {s: 1.0, x: 0, y: 0}}, // zoom out
  {from: {s: 1.045, x: -1.1, y: 0.3}, to: {s: 1.045, x: 1.1, y: -0.3}}, // pan kiri -> kanan
  {from: {s: 1.045, x: 1.1, y: -0.2}, to: {s: 1.045, x: -1.1, y: 0.2}}, // pan kanan -> kiri
];

/**
 * Full-frame documentary image plate with gentle Ken Burns motion.
 * `baseScaleOffset` adds uniform overscan when source art has paper borders.
 */
export const DocumentaryScene: React.FC<{
  src: string;
  index: number;
  durationInFrames: number;
  baseScaleOffset?: number;
}> = ({src, index, durationInFrames, baseScaleOffset = 0}) => {
  const frame = useCurrentFrame();
  const m = MOTIONS[index % MOTIONS.length];
  const p = interpolate(frame, [0, Math.max(1, durationInFrames)], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const s = m.from.s + (m.to.s - m.from.s) * p + baseScaleOffset;
  const x = m.from.x + (m.to.x - m.from.x) * p;
  const y = m.from.y + (m.to.y - m.from.y) * p;

  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: '#241F1A'}}>
      <Img
        src={src}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `translate3d(${x}%, ${y}%, 0) scale(${s})`,
          willChange: 'transform',
        }}
      />
    </AbsoluteFill>
  );
};

