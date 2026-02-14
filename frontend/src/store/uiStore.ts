import { create } from 'zustand';

interface UIState {
    currentUser: { id: string; name: string } | null;
    isConnected: boolean;
    isDragging: boolean;
    selection: string | null; // Selected player ID or other entity ID

    // Actions
    setCurrentUser: (user: { id: string; name: string }) => void;
    setIsConnected: (status: boolean) => void;
    setIsDragging: (status: boolean) => void;
    setSelection: (id: string | null) => void;
}

export const useUIStore = create<UIState>((set) => ({
    currentUser: null,
    isConnected: false,
    isDragging: false,
    selection: null,

    setCurrentUser: (user) => set({ currentUser: user }),
    setIsConnected: (status) => set({ isConnected: status }),
    setIsDragging: (status) => set({ isDragging: status }),
    setSelection: (id) => set({ selection: id }),
}));
