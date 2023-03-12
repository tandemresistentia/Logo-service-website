from django.shortcuts import render
from .test import *
# Create your views here.
def home(request):

    return render(request,'home.html')
def about(request):
    return render(request,'about.html')
