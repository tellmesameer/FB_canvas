import React from 'react';
import { Outlet } from 'react-router-dom';

export const Layout: React.FC = () => {
    return (
        <div className="flex h-screen bg-gray-100 overflow-hidden">
            {/* Sidebar */}
            <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
                <div className="p-4 border-b border-gray-200">
                    <h1 className="text-xl font-bold text-gray-800">Football Canvas</h1>
                </div>
                <nav className="flex-1 p-4">
                    {/* Tool palette will go here */}
                    <div className="text-sm text-gray-500">Tools (Coming Soon)</div>
                </nav>
                <div className="p-4 border-t border-gray-200">
                    {/* User info */}
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col relative">
                <header className="h-14 bg-white border-b border-gray-200 flex items-center px-4 justify-between">
                    <div className="font-medium">Room: <span className="text-gray-500">Loading...</span></div>
                    <div className="space-x-2">
                        <button className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">Share</button>
                    </div>
                </header>
                <div className="flex-1 relative bg-green-50 overflow-hidden">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};
