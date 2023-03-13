from django.shortcuts import render
from .tasks import send_mail_func
# Create your views here.

def home(request):
    send_mail_func.delay()
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')
