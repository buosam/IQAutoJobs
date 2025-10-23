# Incident Report: 502 Bad Gateway on Railway Deployment

## Timeline of Events

*   **[Start Time]**: The initial report of "502 Bad Gateway" errors on the production deployment was received.
*   **[Investigation Start]**: An investigation was initiated to determine the root cause of the errors.
*   **[Initial Hypothesis]**: The initial investigation identified a case-sensitivity issue with a `Backend/` directory in the repository, which was hypothesized to be causing a `ModuleNotFoundError` on Railway's case-sensitive filesystem.
*   **[First Fix Attempt]**: The `Backend/` directory was removed, the Gunicorn timeout was adjusted, and a `/healthz` endpoint was added. The changes were deployed, but the "502 Bad Gateway" error persisted.
*   **[Second Hypothesis]**: Further investigation of the logs revealed that the `ModuleNotFoundError: No module named 'backend'` was still occurring. This indicated that the Python import path was not correctly configured, preventing Gunicorn from finding the application module.
*   **[Final Fix]**: The `Procfile` was updated to prepend the current directory to the `PYTHONPATH`, allowing the Python interpreter to locate the `backend` module.
*   **[End Time]**: The final fix was deployed, and the "502 Bad Gateway" error was resolved.

## Impact Scope

*   **Duration**: The incident lasted from the initial report until the final fix was deployed.
*   **Endpoints Affected**: All endpoints served by the Flask application were affected, resulting in a complete outage of the backend service.

## Root Cause(s) with Evidence

The root cause of the "502 Bad Gateway" error was a `ModuleNotFoundError: No module named 'backend'` that occurred when Gunicorn attempted to start the Flask application. This was caused by an incomplete Python import path.

The evidence for this root cause was found in the Railway deployment logs, which clearly showed the `ModuleNotFoundError` traceback.

## Immediate Fixes Applied

The immediate fix was to modify the `web` process in the `Procfile` to prepend the current directory to the `PYTHONPATH`. The new command is:

```
web: PYTHONPATH=. gunicorn wsgi:app --workers 2 --timeout 30 --bind 0.0.0.0:$PORT
```

This change allows the Python interpreter to correctly locate and import the `backend` module, resolving the `ModuleNotFoundError` and allowing the application to start successfully.

## Preventive Actions

*   **Standardized Project Structure**: Ensure that all new Python projects follow a standard, well-documented project structure to avoid import path issues.
*   **Local Testing with Production-like Commands**: Before deploying, test the application locally using the same Gunicorn command that will be used in production. This can help to catch startup errors before they reach the production environment.
*   **Improved Health Checks**: The `/healthz` endpoint that was added will help to quickly identify whether the application is running, but a more comprehensive `/readyz` endpoint that checks database connectivity could provide even better insight into the application's health.
*   **Runbook for Common Errors**: The `runbook.md` that was created should be expanded to include troubleshooting steps for common errors like `ModuleNotFoundError`.
