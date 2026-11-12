import React from 'react';
import {AbsoluteFill, Img, interpolate, useCurrentFrame} from 'remotion';

// Ken Burns sangat lembut: skala maksimal ~8%, pan perlahan, arah bergantian
const MOTIONS = [
  {from: {s: 1.0, x: 0, y: 0}, to: {s: 1.08, x: 0, y: 0}}, // zoom in
  {from: {s: 1.08, x: 0, y: 0}, to: {s: 1.0, x: 0, y: 0}}, // zoom out
  {from: {s: 1.06, x: -1.5, y: 0.5}, to: {s: 1.06, x: 1.5, y: -0.5}}, // pan kiri -> kanan
  {from: {s: 1.06, x: 1.5, y: 0}, to: {s: 1.06, x: -1.5, y: 0}}, // pan kanan -> kiri
];

export const SejarahScene: React.FC<{
  src: string;
  index: number;
  durationInFrames: number;
}> = ({src, index, durationInFrames}) => {
  const frame = useCurrentFrame();
  const m = MOTIONS[index % MOTIONS.length];
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const s = m.from.s + (m.to.s - m.from.s) * p;
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
          transform: `translate(${x}%, ${y}%) scale(${s})`,
        }}
      />
    </AbsoluteFill>
  );
};
