python manage.py migrate & gunicorn datamagnum.wsgi & wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &
sudo dpkg -i google-chrome-stable_current_amd64.deb & sudo apt-get install -f & pip install -U "celery[redis]" &
redis-cli & celery -A datamagnum worker --pool=solo -l INFO & celery -A datamagnum beat -l INFO 