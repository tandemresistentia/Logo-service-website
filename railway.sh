python manage.py migrate & gunicorn datamagnum.wsgi & celery -A datamagnum worker --uid 1000 --pool=solo -l INFO &
celery -A datamagnum beat -l --uid 1000 INFO 