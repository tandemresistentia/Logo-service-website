from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from datamagnum import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self):
    for i in range(10):
        print(i)
    return "Done"