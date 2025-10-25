# Incident Report: Homepage 502 Bad Gateway

## Summary

On 2025-10-25, the application's homepage (`/`) began returning a 502 Bad Gateway error on the Railway deployment. This prevented users from accessing the site. The root cause was determined to be a misconfigured deployment process that failed to install the required Python dependencies before starting the application server.

## Root Cause Analysis

The investigation revealed the following:

1.  **Error Symptom**: The homepage returned a 502 Bad Gateway, indicating that the upstream application server (Gunicorn) was not running or was crashing.
2.  **Local Reproduction**: I was able to reproduce the issue locally by attempting to run the application with `python app.py` in a clean environment. This resulted in a `ModuleNotFoundError: No module named 'flask'`, which confirmed that the application could not start without its dependencies.
3.  **Deployment Configuration**: The `Procfile` used for deployment on Railway contained a `web` process that started Gunicorn. However, there was no command to install the Python dependencies from `requirements.txt` before starting the application. The `release` command in the `Procfile` is the standard place for this, but it was not being executed or was failing silently.

The application server was failing to start because the necessary Python libraries (including Flask itself) were not installed in the environment. Gunicorn could not load the `app` object from `app.py`, which caused the Gunicorn process to exit and the Railway proxy to return a 502 error.

## Remediation Plan

The following steps will be taken to resolve the issue:

1.  **Update `Procfile`**: The `release` command in the `Procfile` will be updated to include `pip install -r requirements.txt`. This will ensure that all dependencies are installed before the `web` process is started.
2.  **Deployment**: The updated `Procfile` will be deployed to Railway, which will trigger a new release and install the dependencies.
3.  **Verification**: After deployment, the homepage will be monitored to confirm that it loads successfully and the 502 error is resolved.

## Verification Steps

To verify the fix, the following actions will be taken:

1.  **Local Verification**: Before submitting the change, the application will be run locally to ensure that the updated `Procfile` does not introduce any new issues.
2.  **Post-Deployment Monitoring**: After deploying the fix to Railway, the application logs will be monitored for any startup errors. The homepage URL will be accessed to confirm that it returns a 200 OK status code and renders the expected content.
