import React from 'react';
import { AbsoluteFill, Img } from 'remotion';

export const Scene: React.FC<{
  src: string;
  index?: number;
  durationInFrames?: number;
}> = ({ src }) => {
  return (
    <AbsoluteFill style={{ overflow: 'hidden', backgroundColor: '#FFF7E8' }}>
      <Img
        src={src}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
      />
    </AbsoluteFill>
  );
};
