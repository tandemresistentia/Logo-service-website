from django.shortcuts import render
from .tasks import send_mail_func,test
from celery.result import AsyncResult
# Create your views here.
import json


def home(request):
    with open('json_data.json', encoding='utf-8') as json_file:
        dicts = json.load(json_file)
    res = test.delay()
    status_data = res.status
    id_data = res.id
    task_data = AsyncResult(id_data, app=test)
    get_data = task_data.get()
    variable = {
        'json_data' : dicts['value1'],
        'status_data' : status_data,
        'get_data' : get_data,
    }
    return render(request,'home.html',variable)
def about(request):
    return render(request,'about.html')
