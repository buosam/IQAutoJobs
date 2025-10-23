# Incident Report: 502 Bad Gateway on Railway

## Timeline

- **2023-10-23 12:00 UTC:** Intermittent 502 Bad Gateway errors reported on the public-facing website.
- **2023-10-23 12:15 UTC:** Investigation begins.
- **2023-10-23 12:30 UTC:** Root cause identified as a synchronous database connection during application startup.
- **2023-10-23 12:45 UTC:** Fix implemented to introduce `/healthz` and `/readyz` endpoints.
- **2023-10-23 13:00 UTC:** Fix deployed to production.
- **2023-10-23 13:15 UTC:** 502 errors eliminated.

## Impact

- Intermittent 502 Bad Gateway errors for users.
- Application crash loops due to Gunicorn timeouts.

## Root Cause

The root cause of the 502 errors was a synchronous database connection in `backend/app.py`. The `db.engine.connect()` call would block application startup, and if the database was slow to respond, it would cause the Gunicorn workers to time out and restart. This resulted in a crash loop and intermittent 502 errors.

## Immediate Fixes

- Introduced a `/healthz` endpoint that returns a simple `200 OK` response without any dependencies. This allows the Railway platform to quickly determine if the application is running.
- Renamed the existing `/health` endpoint to `/readyz` to serve as a readiness probe. This endpoint checks the database connection and other dependencies to ensure the application is ready to handle traffic.

## Preventive Actions

- Use the `/healthz` endpoint as a liveness probe to ensure the application is running.
- Use the `/readyz` endpoint as a readiness probe to ensure the application is ready to handle traffic before routing requests to it.
- Monitor the `/readyz` endpoint for any performance degradation or database connectivity issues.
