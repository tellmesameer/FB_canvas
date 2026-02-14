import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, endpoints } from '../../services/api';
// import { useStore } from '../../store/useStore';

export const RoomJoin: React.FC = () => {
    const navigate = useNavigate();
    const [roomId, setRoomId] = useState('');
    const [isCreating, setIsCreating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleCreateRoom = async () => {
        setIsCreating(true);
        setError(null);
        try {
            const response = await api.post(endpoints.rooms.create, {
                room_name: "New Match",
                match_duration_minutes: 90
            });
            const room = response.data.data;
            navigate(`/room/${room.room_id}`);
        } catch (err: any) {
            console.error(err);
            setError("Failed to create room. Please try again.");
        } finally {
            setIsCreating(false);
        }
    };

    const handleJoinRoom = () => {
        if (!roomId.trim()) return;
        // Ideally verify room exists first, but for now just navigate
        navigate(`/room/${roomId}`);
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
                <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">Football Canvas</h1>

                {error && (
                    <div className="bg-red-50 text-red-600 p-3 rounded mb-4 text-sm">
                        {error}
                    </div>
                )}

                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Join Existing Room</label>
                        <div className="flex space-x-2">
                            <input
                                type="text"
                                value={roomId}
                                onChange={(e) => setRoomId(e.target.value)}
                                placeholder="Enter Room ID or Slug"
                                className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                            <button
                                onClick={handleJoinRoom}
                                disabled={!roomId.trim()}
                                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Join
                            </button>
                        </div>
                    </div>

                    <div className="relative flex py-2 items-center">
                        <div className="flex-grow border-t border-gray-200"></div>
                        <span className="flex-shrink-0 mx-4 text-gray-400 text-sm">Or</span>
                        <div className="flex-grow border-t border-gray-200"></div>
                    </div>

                    <button
                        onClick={handleCreateRoom}
                        disabled={isCreating}
                        className="w-full bg-green-600 text-white px-4 py-3 rounded font-medium hover:bg-green-700 disabled:opacity-50 flex justify-center"
                    >
                        {isCreating ? 'Creating...' : 'Create New Room'}
                    </button>
                </div>
            </div>
        </div>
    );
};
