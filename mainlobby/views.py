from django.shortcuts import render
from .tasks import test
from celery.result import AsyncResult
from django.conf import settings # new
from django.http.response import JsonResponse,HttpResponse # new
from django.views.decorators.csrf import csrf_exempt # new
import json

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

    # Add additional fields you want to add to the customer profile
import stripe
stripe.api_key = settings.STRIPE_API_KEY
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerProfile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def _on_update_user(sender, instance, created, **kwargs):

    if created:  # If a new user is created

        # Create Stripe user
        customer = stripe.Customer.create(
            email=instance.email,
            name=instance.get_full_name(),
            metadata={
                'user_id': instance.pk,
                'username': instance.username
            },
            description='Created from Django',
        )

        # Create profile
        profile = CustomerProfile.objects.create(user=instance, stripe_customer_id=customer.id)
        profile.save()


PRODUCTS_STRIPE_PRICING_ID = {
    'product_regular': 'price_1McVfZIQDkGdDbUYT2e4DkjX',
    'product_pro': 'price_1MoY0DIQDkGdDbUY7B7Q3dnX',
    'product_platinum': 'price_1McVgSIQDkGdDbUYgQK63TLr',
}

PRODUCTS_STRIPE_PRODUCTS_ID = {
    'product_regular': 'prod_NNGBiaHKfU1wzw',
    'product_pro': 'prod_NNGCYC1hpTNBjQ',
    'product_platinum': 'prod_NNGCiIjFqFlFTx',
}

from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
stripe.api_key = settings.STRIPE_API_KEY
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse

@login_required
@csrf_exempt
def create_stripe_checkout_session(request, product_name):

    try:
        with open('json_data.json', encoding='utf-8') as json_file:
            dicts = json.load(json_file)
        price0 = float(dicts['price0']) * 100
        price1 = float(dicts['price1']) * 100
        price2 = float(dicts['price2']) * 100
        price0 = int(price0)
        price1 = int(price1)
        price2 = int(price2)
        PRODUCTS_STRIPE_NOW_PRICE = {
            'product_regular': price0,
            'product_pro': price1,
            'product_platinum':  price2,
        }


        stripe.Price.create(
        unit_amount=PRODUCTS_STRIPE_NOW_PRICE[product_name],
        currency="eur",
        product=PRODUCTS_STRIPE_PRODUCTS_ID[product_name],
        )

        Data =(stripe.Price.list(limit=3))
        Data =(Data['data'][0])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            metadata={'product_name': product_name, },
            line_items=[
                {'price': Data['id'], 
                 'quantity': 1, },
            ],
            mode='payment',
            success_url='http://localhost:8000/success',
           cancel_url='http://localhost:8000/cancel',        )

        return JsonResponse({'id': checkout_session.id})

    except Exception as e:
        print(e)
        raise SuspiciousOperation(e)
    

@require_POST
@csrf_exempt
def stripe_webhook_paid_endpoint(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Try to validate and create a local instance of the event
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_SIGNING_SECRET)
    except ValueError as e:
        # Invalid payload
        return SuspiciousOperation(e)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return SuspiciousOperation(e)

  # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        # Make sure is already paid and not delayed
        if checkout_session.payment_status == "paid":
            _handle_successful_payment(checkout_session)

    # Passed signature verification
    return HttpResponse(status=200)

def _handle_successful_payment(checkout_session):
    # Define what to do after the user has successfully paid
    pass