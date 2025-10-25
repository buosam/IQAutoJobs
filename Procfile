release: alembic upgrade head && cd frontend && npm install && npm run build
web: gunicorn app:app --workers 2 --timeout 30 --bind 0.0.0.0:$PORT
