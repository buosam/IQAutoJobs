# Runbook: Railway Flask Application

This runbook provides instructions on how to verify, rollback, and redeploy the Railway Flask application.

## Verification

To verify the application is running correctly, follow these steps:

1.  **Check the `/healthz` endpoint:**
    ```bash
    curl -v https://<your-domain>/healthz
    ```
    This should return a `200 OK` response with the status "OK".

2.  **Check the `/readyz` endpoint:**
    ```bash
    curl -v https://<your-domain>/readyz
    ```
    This should return a `200 OK` response with the database status as "connected".

3.  **Check the Railway logs:**
    - Look for any errors or exceptions in the Railway logs.
    - Ensure the application is not in a crash loop.

## Rollback

To roll back to a previous deployment, follow these steps:

1.  Go to the Railway project dashboard.
2.  Select the service.
3.  Go to the "Deployments" tab.
4.  Select the previous deployment you want to roll back to.
5.  Click the "Rollback" button.

## Redeploy

To redeploy the application, follow these steps:

1.  Push your changes to the Git repository.
2.  Railway will automatically build and deploy the new version of the application.
3.  Monitor the deployment in the Railway dashboard.
4.  Once the deployment is complete, verify the application is running correctly using the steps in the "Verification" section.

## Checklists

### Deployment Checklist

- [ ] Verify the `/healthz` endpoint returns a `200 OK` response.
- [ ] Verify the `/readyz` endpoint returns a `200 OK` response with the database status as "connected".
- [ ] Monitor the Railway logs for any errors or exceptions.
- [ ] Ensure the application is not in a crash loop.

### Rollback Checklist

- [ ] Verify the application has been rolled back to the correct version.
- [ ] Verify the `/healthz` endpoint returns a `200 OK` response.
- [ ] Verify the `/readyz` endpoint returns a `200 OK` response with the database status as "connected".
- [ ] Monitor the Railway logs for any errors or exceptions.
