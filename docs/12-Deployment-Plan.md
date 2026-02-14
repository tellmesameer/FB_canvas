# 12. Deployment & DevOps Plan

## 1. Local Development Environment

### 1.1 Prerequisites
*   Python 3.11+
*   Node.js 18+
*   Redis (Local or Docker)
*   PostgreSQL 15+

### 1.2 Startup Sequence
1.  **Database**: `docker-compose up -d db redis`
2.  **Backend**:
    ```bash
    cd app
    uvicorn main:app --reload --port 8000
    ```
3.  **Frontend**:
    ```bash
    cd ui
    npm run dev
    ```

## 2. Environment Configuration

Managed via `.env` file (not committed).

| Variable | Description | Default/Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | Postgres Connection String | `postgresql://user:pass@localhost:5432/canvas` |
| `REDIS_URL` | Redis Connection String | `redis://localhost:6379/0` |
| `SECRET_KEY` | Flask/FastAPI Secret | `generated-uuid` |
| `CORS_ORIGINS` | Allowed Frontend Origins | `http://localhost:3000` |
| `ENV` | Environment Mode | `development` / `production` |

## 3. Deployment Strategy (Dockerized)

### 3.1 Dockerfile Structure
*   **Multi-stage build**:
    1.  `builder`: Install dependencies, build wheels.
    2.  `runner`: Slim python image, copy wheels.
*   **Entrypoint**: `sh run.sh` (Runs migrations -> starts server).

### 3.2 Redis Setup
*   Production: Managed Redis (e.g., AWS ElastiCache / Redis Cloud).
*   Persistence: RDB Snapshots enabled (every 15 mins).
*   Eviction Policy: `volatile-lru`.

## 4. Logging & Monitoring

### 4.1 Logging
*   **Format**: JSON (for ELK/Splunk).
*   **Levels**:
    *   `INFO`: HTTP requests, Room creation, Match start.
    *   `DEBUG`: Mutation details (Dev only).
    *   `ERROR`: Exceptions, DB failures.

### 4.2 Monitoring (Prometheus/Grafana)
*   **Exporters**: `fastapi-prometheus-instrumentator`.
*   **Key Metrics**:
    *   `active_connections_gauge`
    *   `msg_throughput_counter`
    *   `latency_histogram` (P95, P99)

## 5. Backup Strategy
*   **Database**: Daily `pg_dump` to S3 buckets. Retention: 7 days.
*   **Redis**: Not backed up (Ephemeral/Cache only). Start-up rebuilds state from DB.
