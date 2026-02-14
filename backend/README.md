# Backend - Real-Time Collaborative Football Tactical Canvas

This directory contains the Python/FastAPI backend for the application.

## 1. Documentation Map

*   **Architecture & Design**: [05-Backend-TDD.md](../docs/05-Backend-TDD.md)
*   **API Specification**: [04-REST-API-Spec.md](../docs/04-REST-API-Spec.md)
*   **WebSocket Protocol**: [03-WebSocket-Protocol-Spec.md](../docs/03-WebSocket-Protocol-Spec.md)
*   **Database Schema**: [10-Database-Schema-Spec.md](../docs/10-Database-Schema-Spec.md)

## 2. Prerequisites

*   Python 3.11+
*   Redis (for pub/sub and ephemeral state)
*   SQLite (for persistence)

## 3. Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## 4. Running the Server

```bash
# Start the server with hot reload
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
API Docs (Swagger UI) at `http://localhost:8000/docs`.

## 5. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app
```

## 6. Directory Structure

```
backend/
├── app/
│   ├── main.py          # Application entry point
│   ├── api/             # REST API routes
│   ├── socket/          # WebSocket handlers
│   ├── core/            # Config, security, utils
│   ├── models/          # Pydantic models & DB schemas
│   └── services/        # Business logic
├── tests/               # Test suite
└── requirements.txt     # Dependencies
```
