# Project Setup

This project consists of a Python Flask backend and a Next.js frontend.

## Development Setup

### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Flask application:
    ```bash
    flask run
    ```

### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install the required dependencies:
    ```bash
    npm install
    ```
3.  Run the Next.js development server:
    ```bash
    npm run dev
    ```

## Production Build

To prepare the application for production, run the unified build script from the root directory:

```bash
bash build.sh
```

This script will:
1.  Install backend dependencies.
2.  Install frontend dependencies.
3.  Create a production-ready build of the frontend in the `frontend/out` directory.

After the build is complete, the Flask application will serve the frontend. You can start the server using the `Procfile`'s web command:

```bash
gunicorn --chdir backend wsgi:app
```
