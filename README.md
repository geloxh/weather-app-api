### Weather App API
Provider-agnostic weather API built with FastAPI. Ships with an Open-Meteo integration (free, no API key needed) 
behind a normalized schema, so you can ad/swap providers later without touching routers or clients.

### Requirements
```bash
pip install
```
- **fastapi**
- **uvicorn[standard]**
- **httpx**
- **pydantic**
- **pydantic-settings**
- **redis**
# dev / testing
- **pytest**
- **pytest-asyncio**
- **respx**

### Quick start (local, no Docker)
```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\activate
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive Swagger docs.

Without `REDIS_URL` set, caching falls back to an in-mempry store - fine for local dev,
not for multi-process production deployments.

### Quick start (Docker, with Redis)
```bash
docker compose up --build
```

This runs the API + Redis together, with hot-reload on code changes.

## Endpoints
| Endpoints | Description |
|-----------|-------------|
|              `GET /health`                   |      Health Check    |
|         `GET /v1/current?lat=&lon=`          |   Current conditions |
| `GET /v1/forecast/hourly?lat=&lon=&hours=48` |    Hourly forecast   |
| `GET /v1/forecast/daily?lat=&lon=&hours=48`  |     Daily forecast   |
|         `GET /v1/search?query=`              | Geocode a place name |


### geloxh