from django.shortcuts import render
from .tasks import test
from celery.result import AsyncResult
# Create your views here.
import json
import stripe
from django.conf import settings # new
from django.http.response import JsonResponse,HttpResponse # new
from django.views.decorators.csrf import csrf_exempt # new

def home(request):
    with open('json_data.json', encoding='utf-8') as json_file:
        dicts = json.load(json_file)
    variable = {
      'type0':dicts['type0'],
      'price0':dicts['price0'],
      'desc0':dicts['desc0'],
      'package_time0':dicts['package_time0'],
      'package_row0':dicts['package_row0'],
      'package_row3':dicts['package_row3'],
      'package_row6':dicts['package_row6'],
      'package_row9':dicts['package_row9'],
      'package_row12':dicts['package_row12'],
      'package_row15':dicts['package_row15'],
      'package_row18':dicts['package_row18'],
      
      

      'type1':dicts['type1'],
      'price1':dicts['price1'],
      'desc1':dicts['desc1'],
      'package_time1':dicts['package_time1'],
      'package_row1':dicts['package_row1'],
      'package_row4':dicts['package_row4'],
      'package_row7':dicts['package_row7'],
      'package_row10':dicts['package_row10'],
      'package_row13':dicts['package_row13'],
      'package_row16':dicts['package_row16'],
      'package_row19':dicts['package_row19'],
      

      'type2':dicts['type2'],
      'price2':dicts['price2'],
      'desc2':dicts['desc2'],
      'package_time2':dicts['package_time2'],
      'package_row2':dicts['package_row2'],
      'package_row5':dicts['package_row5'],
      'package_row8':dicts['package_row8'],
      'package_row11':dicts['package_row11'],
      'package_row14':dicts['package_row14'],
      'package_row17':dicts['package_row17'],
      'package_row20':dicts['package_row20'],
      
      'revisions':dicts['revisions'],
      }
    return render(request,'home.html',variable)
def about(request):
    return render(request,'about.html')

#success view
def success(request):
 return render(request,'success.html')

 #cancel view
def cancel(request):
 return render(request,'cancel.html')

stripe.api_key = settings.STRIPE_PRIVATE_KEY
from django.urls import reverse

@csrf_exempt
def checkout(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1McVfZIQDkGdDbUYT2e4DkjX',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )

    return JsonResponse({
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    })