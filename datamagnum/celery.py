from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datamagnum.settings')

app = Celery('datamagnum')
app.conf.enable_utc = False

app.conf.update(timezone = 'UTC')

app.config_from_object(settings, namespace='CELERY')
from celery.schedules import crontab
# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-every-day-at-8': {
        'task': 'mainlobby.tasks.test',
        'schedule': crontab(minute=0, hour=1),
        #'args': (2,)
    }
    
}

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')