release: alembic -c backend/alembic.ini upgrade head
web: PYTHONPATH=. gunicorn wsgi:app --workers 2 --timeout 30 --bind 0.0.0.0:$PORT
