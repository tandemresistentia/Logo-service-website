python manage.py migrate & gunicorn datamagnum.wsgi & sudo apt install -y chromium-browser &
redis-cli & celery -A datamagnum worker --pool=solo -l INFO & celery -A datamagnum beat -l INFO 