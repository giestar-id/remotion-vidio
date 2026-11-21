import React from 'react';
import {AbsoluteFill, Img} from 'remotion';

export const SejarahScene: React.FC<{
  src: string;
  index?: number;
  durationInFrames?: number;
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
