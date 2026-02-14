import React, { useEffect, useRef, useState } from 'react';
import { Stage, Layer, Text } from 'react-konva';
import { useParams } from 'react-router-dom';
import { useCanonicalStore } from '../../store/canonicalStore';
import { useUIStore } from '../../store/uiStore';
import { wsService } from '../../services/websocket';
import { api, endpoints } from '../../services/api';
import { FieldLayer } from './layers/FieldLayer';
import { PlayersLayer } from './layers/PlayersLayer';

export const TacticalBoard: React.FC = () => {
    const { roomId } = useParams<{ roomId: string }>();
    const stageRef = useRef(null);
    const [size, setSize] = useState({ width: window.innerWidth, height: window.innerHeight });
    const [error, setError] = useState<string | null>(null);

    const setSnapshot = useCanonicalStore((state) => state.setSnapshot);
    const { currentUser, setCurrentUser } = useUIStore();

    // Resize handler
    useEffect(() => {
        const handleResize = () => {
            setSize({ width: window.innerWidth - 256, height: window.innerHeight - 56 });
        };
        window.addEventListener('resize', handleResize);
        handleResize();
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    // Initial Fetch & WebSocket Connect
    useEffect(() => {
        if (!roomId) return;

        // Fetch initial state
        const fetchRoom = async () => {
            try {
                const response = await api.get(endpoints.rooms.get(roomId));
                setSnapshot(response.data.data);
                setError(null); // Clear any previous errors on successful fetch

                // Auto-generate a user ID if not present
                let user = currentUser;
                if (!user) {
                    user = { id: `user-${Math.floor(Math.random() * 10000)}`, name: 'Coach' };
                    setCurrentUser(user);
                }

                // Connect WS
                wsService.connect(roomId, user.id);

                return () => {
                    // Cleanup handled by WS service internally or we could add disconnect method
                };
            } catch (err: any) {
                console.error("Failed to load room", err);
                // Optionally set error in UI store or local state
                // For now, let's just log it, but ideally we show it on canvas
                setError(err.message || "Failed to load room data."); // Set error state
                useUIStore.getState().setSelection("error"); // overloading selection for quick test or add setError to UIStore
            }
        };

        fetchRoom();
    }, [roomId]);

    return (
        <Stage width={size.width} height={size.height} ref={stageRef} draggable>
            <FieldLayer />
            <PlayersLayer />
            <Layer>
                {/* Debug/UI Overlay Layer - could be separate too */}
                {!useCanonicalStore.getState().room && (
                    <Text text="Loading Room..." x={50} y={50} fontSize={24} fill="white" />
                )}
                {/* Error Overlay */}
                {error && (
                    <Text
                        text={`Error: ${error}`}
                        x={size.width / 2 - 200}
                        y={size.height / 2}
                        fontSize={24}
                        fill="red"
                        width={400}
                        align="center"
                    />
                )}
            </Layer>
        </Stage>
    );
};
