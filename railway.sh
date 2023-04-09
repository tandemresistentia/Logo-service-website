python manage.py migrate && gunicorn datamagnum.wsgi 
celery -A datamagnum worker --pool=solo -l INFO
celery -A datamagnum beat -l INFO
stripe listen --forward-to https://web-production-b540.up.railway.app/stripe-webhook-paid/ 