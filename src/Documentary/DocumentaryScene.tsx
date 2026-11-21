import React from 'react';
import {AbsoluteFill, Img} from 'remotion';

/**
 * Full-frame documentary image plate (Hard-cut statik murni tanpa gerakan/transisi).
 */
export const DocumentaryScene: React.FC<{
  src: string;
  index?: number;
  durationInFrames?: number;
  baseScaleOffset?: number;
}> = ({src}) => {
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: '#241F1A'}}>
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
