from django.contrib.auth import get_user_model
import json
from celery import shared_task
from django.core.mail import send_mail
from datamagnum import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self):
    data = 'Hello'

    # .dumps() as a string
    json_string = json.dumps(data)
    print(json_string)
    with open('json_data.json', 'w') as outfile:
        outfile.write(json_string)
    return data

@shared_task(bind=True)
def test(self):
    data = 'Hello'
    print(data)
    return data