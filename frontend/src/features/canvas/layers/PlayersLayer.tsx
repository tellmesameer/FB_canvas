import React from 'react';
import { Layer } from 'react-konva';
import { PlayerToken } from '../PlayerToken';
import { useCanonicalStore } from '../../../store/canonicalStore';
import { useUIStore } from '../../../store/uiStore';
import { wsService } from '../../../services/websocket';

export const PlayersLayer: React.FC = () => {
    const room = useCanonicalStore((state) => state.room);
    const updatePlayer = useCanonicalStore((state) => state.updatePlayer);
    const setIsDragging = useUIStore((state) => state.setIsDragging);

    const handleDragStart = () => {
        setIsDragging(true);
    };

    const handleDragEnd = (playerId: string, x: number, y: number) => {
        setIsDragging(false);
        const player = room?.teams.flatMap(t => t.players).find(p => p.player_id === playerId);

        if (player) {
            const updatedPlayer = { ...player, x, y };
            // Optimistic update
            updatePlayer(updatedPlayer);

            // Send throttled or direct update
            // For end of drag, we can send directly
            wsService.send({
                type: 'player_moved',
                player: updatedPlayer
            });
        }
    };

    // For drag move (continuous), we would need onDragMove handler and use sendThrottled
    // But PlayerToken currently exposes onDragEnd. 
    // Implementing onDragMove in PlayerToken or here would enable live syncing.

    if (!room) return null;

    return (
        <Layer>
            {room.teams.flatMap(team =>
                team.players.map(player => (
                    <PlayerToken
                        key={player.player_id}
                        id={player.player_id}
                        x={player.x}
                        y={player.y}
                        teamColor={team.color}
                        label={player.label || player.role}
                        onDragStart={handleDragStart}
                        onDragEnd={handleDragEnd}
                    />
                ))
            )}
        </Layer>
    );
};
