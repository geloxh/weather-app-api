# Weather Forecast App — Project Plan
Developing independent Weather API for w Weather App.

### Python Weather API · Web App · Mobile App

**Approach:** Build the Python API first as a standalone service (it's the shared dependency), then develop Web and Mobile in parallel once the API contract is stable. Assumes a small team (2–5 people) building an MVP first, then scaling. Adjust timelines to your team size.

---

## 0. System Overview

```
                     ┌─────────────────────┐
                     │  External Providers  │
                     │ (NOAA, OpenWeather,   │
                     │  Tomorrow.io, etc.)   │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │   Python Weather API  │
                     │  (FastAPI + Redis +   │
                     │   PostgreSQL/PostGIS) │
                     └───┬───────────────┬───┘
                         │               │
                ┌────────▼───┐     ┌─────▼────────┐
                │   Web App    │     │  Mobile App   │
                │  (Next.js)   │     │ (React Native/│
                │              │     │     Expo)     │
                └──────────────┘     └───────────────┘
```

Each of the three tracks below is written as an independent project plan with its own phases, so you can run them as separate epics/boards, but they share the API contract (OpenAPI schema) as the integration point.

---

## Track 1 — Python Weather API

### Goals
- Aggregate and normalize data from one or more upstream weather providers.
- Serve fast, cached, geospatially-aware endpoints to both Web and Mobile.
- Be provider-agnostic (swap/blend providers without breaking clients).

### Tech Stack
- **Framework:** FastAPI (async, auto-generated OpenAPI docs, Pydantic validation)
- **Database:** PostgreSQL + PostGIS extension (location/geospatial queries, saved locations, alert zones)
- **Cache:** Redis (cache weather responses per lat/lng grid cell, TTL 10–30 min depending on data type)
- **Task queue:** Celery or APScheduler (periodic data refresh, push notification triggers)
- **Auth:** OAuth2/JWT (via `fastapi-users` or custom) if you need user accounts for saved locations/alerts
- **Deployment:** Docker container → AWS ECS/Fargate, Render, Railway, or Fly.io (skip Kubernetes until you actually need it)
- **Testing:** pytest + httpx for async endpoint testing
- **Docs:** Auto-generated via FastAPI's OpenAPI/Swagger

### Data Model (core entities)
- `Location` (lat, lng, name, timezone, PostGIS point)
- `CurrentConditions` (temp, humidity, wind, pressure, condition code, timestamp)
- `ForecastDaily` / `ForecastHourly`
- `Alert` (severe weather alerts by region)
- `User` + `SavedLocation` (if accounts are in scope)
- `ProviderCache` (raw upstream responses, for debugging/fallback)

### API Endpoints (v1 draft)
| Endpoint | Purpose |
|---|---|
| `GET /v1/current?lat=&lng=` | Current conditions |
| `GET /v1/forecast/hourly?lat=&lng=` | Hourly forecast (48–72hr) |
| `GET /v1/forecast/daily?lat=&lng=` | Daily forecast (7–14 day) |
| `GET /v1/alerts?lat=&lng=` | Active severe weather alerts |
| `GET /v1/search?query=` | Geocoding / location search |
| `POST /v1/users/locations` | Save a favorite location (auth required) |
| `GET /v1/radar?lat=&lng=` | Radar tile/image data (if in scope) |

### Phases

**Phase 1 — Foundation (Week 1–2)**
- Set up FastAPI project structure, Docker, CI pipeline (GitHub Actions)
- Integrate first upstream provider (e.g., Open-Meteo or OpenWeatherMap — pick one to start)
- Basic `/current` and `/forecast` endpoints, no caching yet
- Deploy skeleton to staging environment

**Phase 2 — Core Data Layer (Week 3–4)**
- Add PostgreSQL + PostGIS for location storage
- Implement Redis caching layer with sensible TTLs
- Normalize provider response into your own internal schema (so you can swap providers later without breaking clients)
- Add geocoding/search endpoint

**Phase 3 — Reliability & Scale (Week 5–6)**
- Add second provider as fallback (blend/failover logic)
- Rate-limit handling and retry logic for upstream calls
- Load testing (locust or k6) to find real bottlenecks
- Add alerts endpoint + background job to poll for severe weather

**Phase 4 — Auth & Personalization (Week 7–8, if in scope)**
- User accounts, saved locations, notification preferences
- Push notification trigger service (hooks into FCM)

**Phase 5 — Hardening (ongoing)**
- Observability (Sentry, Prometheus/Grafana or Datadog)
- API versioning strategy
- Documentation for frontend teams (published OpenAPI spec)

### Milestone deliverable
A versioned, documented REST API (`/v1/...`) deployed to staging with >99% uptime target, cache hit rate tracked, and OpenAPI schema published for the frontend teams to consume/generate typed clients from.

---

### geloxh