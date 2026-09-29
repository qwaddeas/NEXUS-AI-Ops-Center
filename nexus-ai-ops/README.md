# NEXUS — AI Operations Center v2.0

Portfolio-grade AI + DevOps observability dashboard.

## Highlights
- **Real-time WebSocket telemetry** every 2 seconds
- Live CPU / memory / request / latency cards
- Service mesh health view
- Incident stream
- AI incident diagnosis workflow
- Prometheus metrics endpoint
- Docker Compose infrastructure
- PostgreSQL + Redis services ready for persistence/caching
- GitHub Actions CI
- Responsive dark operations UI

## Architecture

```text
Browser (React/TS)
       │
       ├── REST ──────► FastAPI ───► AI / metrics
       │                    │
       └── WebSocket ◄──────┘
                            │
                   ┌────────┴────────┐
                   ▼                 ▼
              PostgreSQL          Redis
                   │
                   ▼
               Prometheus
```

## Run locally

```bash
docker compose up --build
```

- Dashboard: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Prometheus: http://localhost:9090

The current AI analyzer is deterministic/demo-safe. Add an LLM provider later behind the same endpoint without changing the dashboard.
