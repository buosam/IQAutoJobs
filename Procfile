release: alembic -c backend/alembic.ini upgrade head
web: gunicorn wsgi:app --workers ${WEB_CONCURRENCY:-2} --threads ${GUNICORN_THREADS:-4} --timeout 120 --bind 0.0.0.0:$PORT
