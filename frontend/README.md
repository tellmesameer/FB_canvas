# Frontend - Real-Time Collaborative Football Tactical Canvas

This directory contains the React/TypeScript frontend for the application.

## 1. Documentation Map

*   **Frontend Architecture**: [06-Frontend-TDD.md](../docs/06-Frontend-TDD.md)
*   **Visual Requirements**: [01-BRD.md](../docs/01-BRD.md)
*   **WebSocket Integration**: [03-WebSocket-Protocol-Spec.md](../docs/03-WebSocket-Protocol-Spec.md)

## 2. Prerequisites

*   Node.js 18+
*   npm or yarn

## 3. Setup

```bash
# Install dependencies
npm install
```

## 4. Running Development Server

```bash
# Start dev server
npm run dev
```

The application will be available at `http://localhost:5173`.

## 5. Running Tests

```bash
# Run unit tests
npm run test

# Run e2e tests
npm run test:e2e
```

## 6. Build for Production

```bash
# Build the application
npm run build

# Preview production build
npm run preview
```

## 7. Directory Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── features/        # Feature-based modules (Canvas, Room, etc.)
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API and WebSocket services
│   ├── store/           # Zustand state stores
│   ├── types/           # TypeScript definitions
│   └── utils/           # Helper functions
├── public/              # Static assets
└── package.json         # Dependencies and scripts
```
