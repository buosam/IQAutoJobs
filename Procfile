release: alembic -c backend/alembic.ini upgrade head
web: gunicorn wsgi:app --workers 2 --timeout 60 --bind 0.0.0.0:$PORT
