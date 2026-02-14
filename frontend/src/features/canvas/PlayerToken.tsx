import React, { useRef } from 'react';
import { Circle, Text, Group } from 'react-konva';

interface PlayerTokenProps {
    id: string;
    x: number;
    y: number;
    teamColor: string;
    label?: string;
    isDraggable?: boolean;
    onDragStart?: (id: string) => void;
    onDragEnd?: (id: string, x: number, y: number) => void;
}

export const PlayerToken: React.FC<PlayerTokenProps> = ({
    id, x, y, teamColor, label, isDraggable = true, onDragStart, onDragEnd
}) => {
    const groupRef = useRef<any>(null);

    return (
        <Group
            x={x}
            y={y}
            draggable={isDraggable}
            ref={groupRef}
            onDragStart={() => {
                onDragStart?.(id);
            }}
            onDragEnd={(e) => {
                onDragEnd?.(id, e.target.x(), e.target.y());
            }}
            onMouseEnter={() => {
                if (isDraggable) document.body.style.cursor = 'pointer';
            }}
            onMouseLeave={() => {
                document.body.style.cursor = 'default';
            }}
        >
            <Circle
                radius={15}
                fill={teamColor}
                stroke="white"
                strokeWidth={2}
                shadowBlur={5}
                shadowOpacity={0.3}
            />
            {label && (
                <Text
                    text={label}
                    fontSize={12}
                    fill="white"
                    align="center"
                    verticalAlign="middle"
                    offsetX={5}
                    offsetY={5}
                    fontStyle="bold"
                />
            )}
        </Group>
    );
};
