import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './features/layout/Layout';

// Lazy load components
const TacticalBoard = React.lazy(() => import('./features/canvas/TacticalBoard').then(module => ({ default: module.TacticalBoard })));
const RoomJoin = React.lazy(() => import('./features/room/RoomJoin').then(module => ({ default: module.RoomJoin })));

// Loading fallback
const Loading = () => <div className="flex items-center justify-center h-full">Loading...</div>;

function App() {
  return (
    <Router>
      <Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/" element={<Navigate to="/join" replace />} />
          <Route path="/join" element={<RoomJoin />} />
          <Route path="/room/:roomId" element={<Layout />}>
            <Route index element={<TacticalBoard />} />
          </Route>
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;
