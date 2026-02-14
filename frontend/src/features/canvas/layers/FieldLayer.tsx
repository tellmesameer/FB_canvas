import React from 'react';
import { Layer, Rect, Circle } from 'react-konva';

export const FieldLayer: React.FC = () => {
    return (
        <Layer>
            {/* Pitch Background */}
            <Rect
                x={0}
                y={0}
                width={1200}
                height={800}
                fill="#4ade80" // Green-400
                stroke="white"
                strokeWidth={4}
            />
            {/* Center Circle */}
            <Circle x={600} y={400} radius={70} stroke="white" strokeWidth={4} />
            {/* Center Line */}
            <Rect x={600} y={0} width={4} height={800} fill="white" />
        </Layer>
    );
};
