export type MatchStatus = 'setup' | 'live' | 'expired' | 'archived';
export type TeamSide = 'home' | 'away';

export interface Player {
    player_id: string;
    team_id: string;
    room_id: string;
    x: number;
    y: number;
    label?: string;
    role?: string;
    is_goalkeeper: boolean;
}

export interface Team {
    team_id: string;
    room_id: string;
    name: string;
    color: string;
    side: TeamSide;
    players: Player[];
}

export interface Room {
    room_id: string;
    slug: string;
    match_status: MatchStatus;
    created_at: string;
    expires_at?: string;
    version: number;
    teams: Team[];
}

// Store types
export interface CanonicalState {
    room: Room | null;
    players: Record<string, Player>; // Map for easier access? Or keep array?
    // Array is easier to sync with server, but Map easier for updates.
    // The backend sends full snapshots or updates.
    // Let's stick to Room structure which contains teams and players.
}
