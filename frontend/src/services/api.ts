import axios from 'axios';

// Use environment variable for base URL or default to localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const endpoints = {
    rooms: {
        create: '/rooms/',
        get: (id: string) => `/rooms/${id}`,
        join: (id: string) => `/rooms/${id}/join`, // If implemented
    },
    teams: {
        list: (roomId: string) => `/rooms/${roomId}/teams/`,
        update: (roomId: string, teamId: string) => `/rooms/${roomId}/teams/${teamId}`,
    },
    match: {
        start: (roomId: string) => `/rooms/${roomId}/match/start`,
        end: (roomId: string) => `/rooms/${roomId}/match/end`,
    },
};
