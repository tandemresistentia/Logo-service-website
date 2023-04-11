wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&
sudo apt-get update && sudo apt-get install -y libappindicator1 && sudo apt install -y google-chrome-stable_current_amd64.deb &&
python manage.py migrate & gunicorn datamagnum.wsgi &
redis-cli & celery -A datamagnum worker --pool=solo -l INFO & celery -A datamagnum beat -l INFO 