# Store Locator Service

An end-to-end FastAPI application for searching nearby retail locations and securely managing store data with role-based access control.

## Framework & Libraries
- **Framework:** FastAPI
- **ORM:** SQLModel (SQLAlchemy)
- **Auth:** PyJWT + bcrypt
- **Geo:** Manual Haversine distance + Nominatim HTTP geocoding
- **CSV:** Python `csv` module
- **Cache/Rate Limit:** In-memory (Redis-ready hooks)

## Quickstart
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy environment template and adjust as needed:
   ```bash
   cp .env.example .env
   ```
3. Start the API (uses SQLite by default):
   ```bash
   uvicorn store_locator.main:app --reload
   ```
4. Open API docs: `http://localhost:8000/docs`

## Configuration
See `.env.example` for all tunables. Key values:
- `DATABASE_URL` (e.g., `postgresql+psycopg2://user:pass@localhost/dbname`)
- `JWT_SECRET_KEY`
- `ACCESS_TOKEN_EXP_MINUTES`, `REFRESH_TOKEN_EXP_DAYS`
- `GEOCODING_USER_AGENT`

## Database & Seeding
- Tables cover stores, store services, users, roles, permissions, and refresh tokens.
- On startup the app creates tables and seeds:
  - Roles: **Admin**, **Marketer**, **Viewer**
  - Users: `admin@test.com`, `marketer@test.com`, `viewer@test.com` (passwords in `project_description.md`)
  - Sample stores from `stores_50.csv`

## Core Endpoints
- `POST /api/stores/search` – Public search by address/ZIP/coordinates with radius, service, type, and open filters.
- Admin endpoints (authenticated via `Authorization: Bearer <access_token>`):
  - CRUD: `/api/admin/stores`, `/api/admin/stores/{store_id}`
  - CSV import (upsert): `/api/admin/stores/import`
  - Users: `/api/admin/users`
  - Auth: `/api/admin/auth/login|refresh|logout`
- Health: `/health`

## Authentication & RBAC
- Access token TTL: 15 minutes; Refresh: 7 days.
- Refresh tokens are hashed and stored for revocation.
- Roles and permissions enforced via dependency guards.

## Search Logic
- Bounding-box prefilter + precise Haversine calculation.
- Services filter (AND), store types (OR), optional `open_now`.
- Caching: geocoding (30 days) and search results (10 minutes).
- Rate limiting: per-IP (10/min, 100/hour).

## CSV Import
- Accepts the exact column order defined in `project_description.md`.
- Validates coordinates and hours; upserts stores; returns summary counts.

## Testing
Run the automated tests:
```bash
pytest
```

## Deployment Notes
- For PostgreSQL, set `DATABASE_URL` accordingly; SQLModel handles schema creation.
- Use a production ASGI server (e.g., Gunicorn + Uvicorn workers).
- Swap the in-memory caches/rate-limits with Redis for multi-instance deployments.
