# Runbook: Flask Application on Railway

This document provides standard operating procedures for maintaining the Flask backend service on Railway.

## 1. Verification Steps

After any deployment, follow these steps to ensure the application is healthy.

### 1.1. Check Deployment Logs

1.  Open the Railway dashboard and navigate to the `backend` service.
2.  Review the latest deployment logs for any errors, stack traces, or crash loops.
3.  **Success Criteria**: The log output should show the Gunicorn server starting and listening on the correct port (e.g., `Listening at: http://0.0.0.0:XXXX`).

### 1.2. Check Health Endpoint

1.  Make a `curl` request to the health check endpoint.
    ```bash
    curl -v https://[deployment-domain]/healthz
    ```
2.  **Success Criteria**: The command should return an HTTP `200 OK` status code.

### 1.3. Monitor for Errors

1.  Observe the application logs for 5-10 minutes after deployment.
2.  **Success Criteria**: There should be no new 5xx errors or crash reports.

## 2. Rollback Procedure

If a deployment introduces a critical bug, roll back to the previous stable version immediately.

1.  Go to the service's **Deployments** tab in Railway.
2.  Find the last known good deployment in the list.
3.  Click the **Redeploy** button for that specific deployment.
4.  Monitor the logs to ensure the rollback is successful.

## 3. Redeployment Procedure

To redeploy the latest commit from the `main` branch (e.g., after a hotfix):

1.  Ensure the code has been merged to the `main` branch in Git.
2.  In the Railway dashboard, trigger a new deployment manually or rely on the automatic deployment trigger.
3.  Follow the **Verification Steps** above to confirm the new deployment is stable.
