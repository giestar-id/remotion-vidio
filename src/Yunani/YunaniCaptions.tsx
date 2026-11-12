import React from 'react';
import type {Caption} from '@remotion/captions';
import {
  DocumentaryCaptions,
  DocumentaryDecorations,
  EraLowerThirds,
  type DocumentaryHeaderConfig,
  type EraMarker,
} from '../Documentary';

const DEFAULT_YUNANI_HEADER: DocumentaryHeaderConfig = {
  headerTitle: 'SEJARAH YUNANI',
  channelName: 'SEJARAONE',
};

export type {EraMarker};
export {EraLowerThirds};

export const YunaniCaptions: React.FC<{captions: Caption[]}> = ({captions}) => (
  <DocumentaryCaptions captions={captions} />
);

export const YunaniDecorations: React.FC = () => (
  <DocumentaryDecorations config={DEFAULT_YUNANI_HEADER} />
);
