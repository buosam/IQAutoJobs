release: alembic -c backend/alembic.ini upgrade head
web: gunicorn wsgi:app --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT
