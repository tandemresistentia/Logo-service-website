python manage.py migrate & gunicorn datamagnum.wsgi & 
redis-cli & celery -A datamagnum worker --pool=solo -l INFO & celery -A datamagnum beat -l INFO 