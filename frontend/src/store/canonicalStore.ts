import { create } from 'zustand';
import type { Room, Player, Team, MatchStatus } from '../types';

interface CanonicalState {
    room: Room | null;
    version: number;
    matchStatus: MatchStatus;

    // Actions
    setSnapshot: (room: Room) => void;
    updatePlayer: (player: Player) => void;
    updateTeam: (team: Team) => void;
    setMatchStatus: (status: MatchStatus) => void;
}

export const useCanonicalStore = create<CanonicalState>((set) => ({
    room: null,
    version: 0,
    matchStatus: 'setup',

    setSnapshot: (room) => set({
        room,
        version: room.version,
        matchStatus: room.match_status
    }),

    updatePlayer: (updatedPlayer) => set((state) => {
        if (!state.room) return state;

        const newTeams = state.room.teams.map(team => {
            if (team.team_id === updatedPlayer.team_id) {
                const playerIndex = team.players.findIndex(p => p.player_id === updatedPlayer.player_id);
                let newPlayers = [...team.players];
                if (playerIndex >= 0) {
                    newPlayers[playerIndex] = updatedPlayer;
                } else {
                    newPlayers.push(updatedPlayer);
                }
                return { ...team, players: newPlayers };
            }
            return team;
        });

        return {
            room: { ...state.room, teams: newTeams },
            // version might need incrementing if we were tracking it locally strictly, 
            // but usually server sends the new version in the update message.
            // For now, we assume optimistic updates don't change version until server confirms.
        };
    }),

    updateTeam: (updatedTeam) => set((state) => {
        if (!state.room) return state;
        const newTeams = state.room.teams.map(t => t.team_id === updatedTeam.team_id ? updatedTeam : t);
        return { room: { ...state.room, teams: newTeams } };
    }),

    setMatchStatus: (status) => set((state) => {
        if (!state.room) return state;
        return {
            matchStatus: status,
            room: { ...state.room, match_status: status }
        };
    }),
}));
