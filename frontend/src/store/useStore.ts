import { create } from 'zustand';
import type { Room, Player, Team } from '../types';

interface AppState {
    // Canonical State (Synced with Server)
    room: Room | null;
    setRoom: (room: Room) => void;
    updatePlayer: (player: Player) => void;
    updateTeam: (team: Team) => void;

    // Local UI State
    currentUser: { id: string; name: string } | null;
    setCurrentUser: (user: { id: string; name: string }) => void;

    isConnected: boolean;
    setIsConnected: (status: boolean) => void;
}

export const useStore = create<AppState>((set) => ({
    room: null,
    setRoom: (room) => set({ room }),

    updatePlayer: (updatedPlayer) => set((state) => {
        if (!state.room) return state;

        // Find team and update player in it
        const newTeams = state.room.teams.map(team => {
            if (team.team_id === updatedPlayer.team_id) {
                const playerIndex = team.players.findIndex(p => p.player_id === updatedPlayer.player_id);
                let newPlayers = [...team.players];
                if (playerIndex >= 0) {
                    newPlayers[playerIndex] = updatedPlayer;
                } else {
                    // Add if not found? 
                    newPlayers.push(updatedPlayer);
                }
                return { ...team, players: newPlayers };
            }
            return team;
        });

        return { room: { ...state.room, teams: newTeams } };
    }),

    updateTeam: (updatedTeam) => set((state) => {
        if (!state.room) return state;
        const newTeams = state.room.teams.map(t => t.team_id === updatedTeam.team_id ? updatedTeam : t);
        return { room: { ...state.room, teams: newTeams } };
    }),

    currentUser: null,
    setCurrentUser: (user) => set({ currentUser: user }),

    isConnected: false,
    setIsConnected: (status) => set({ isConnected: status }),
}));
