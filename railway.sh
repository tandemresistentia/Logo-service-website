python manage.py migrate & gunicorn datamagnum.wsgi & celery -A datamagnum worker --pool=solo -l INFO & celery -A datamagnum beat -l INFO 