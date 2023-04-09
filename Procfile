web: python manage.py migrate && gunicorn datamagnum.wsgi 
celery_worker: celery -A datamagnum worker --pool=solo -l INFO
celery_beat: celery -A datamagnum beat -l INFO
stripe_listen: stripe listen --forward-to https://web-production-b540.up.railway.app/stripe-webhook-paid/ 