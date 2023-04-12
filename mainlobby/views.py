from django.shortcuts import render
from celery.result import AsyncResult
from django.conf import settings # new
from django.http.response import JsonResponse,HttpResponse,FileResponse # new
from django.views.decorators.csrf import csrf_exempt # new
import json
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
try:
    stripe.api_key = settings.STRIPE_API_KEY
except:
    stripe.api_key = settings.TEST_STRIPE_API_KEY
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from .models import Product
from django.core.mail import send_mail
from .forms import NameForm
import datetime
import random
from django.shortcuts import redirect
from .models import Order
import os 
def home(request):
    try:
        global user_email
        user_email = request.user.email
        global user
        user = request.user
    except:
        pass
    i = 0
    global json_data
    try:
        json_data = 'json_data'+str(i)+'.json'
        with open(json_data, encoding='utf-8') as json_file:
            dicts = json.load(json_file)
    except:
        i+=1
        try:
            json_data = 'json_data'+str(i)+'.json'
            with open(json_data, encoding='utf-8') as json_file:
                dicts = json.load(json_file)
        except:
            i+=1
            try:
                json_data = 'json_data'+str(i)+'.json'
                with open(json_data, encoding='utf-8') as json_file:
                    dicts = json.load(json_file)
            except:
                i+=1
                try:
                    json_data = 'json_data'+str(i)+'.json'
                    with open(json_data, encoding='utf-8') as json_file:
                        dicts = json.load(json_file)
                except:
                    i+=1
                    json_data = 'json_data'+str(i)+'.json'
                    with open(json_data, encoding='utf-8') as json_file:
                        dicts = json.load(json_file)
    global price0 
    price0=dicts['price0']
    global price1 
    price1=dicts['price1']
    global price2 
    price2=dicts['price2']
    
    global url_data
    url_data = dicts['url']
    global revisions_data
    revisions_data = dicts['revisions']
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

#success view
def success(request):
 return render(request,'orders/success.html')

 #cancel view
def cancel(request):
 return render(request,'orders/cancel.html')

    # Add additional fields you want to add to the customer profile


PRODUCTS_STRIPE_PRICING_ID = {
    'product_regular': 'price_1MvNFaIQDkGdDbUY0KU0Gm4e',
    'product_pro': 'price_1MvNGFIQDkGdDbUYqGx8czJ5',
    'product_platinum': 'price_1MvNFwIQDkGdDbUYJHQr0HSW',
}

PRODUCTS_STRIPE_PRODUCTS_ID = {
    'product_regular': 'prod_NgklgdcS9FRdq2',
    'product_pro': 'prod_NgklZip6JvzoXq',
    'product_platinum': 'prod_NgklsIdd0RGlCD',
}


@login_required
@csrf_exempt
def create_stripe_checkout_session(request, product_name):
    i = 0
    try:
        with open('json_data'+str(i)+'.json', encoding='utf-8') as json_file:
            dicts = json.load(json_file)
    except:
        i+=1
        try:
            with open('json_data'+str(i)+'.json', encoding='utf-8') as json_file:
                dicts = json.load(json_file)
        except:
            i+=1
            try:
                with open('json_data'+str(i)+'.json', encoding='utf-8') as json_file:
                    dicts = json.load(json_file)
            except:
                i+=1
                try:
                    with open('json_data'+str(i)+'.json', encoding='utf-8') as json_file:
                        dicts = json.load(json_file)
                except:
                    i+=1
                    with open('json_data'+str(i)+'.json', encoding='utf-8') as json_file:
                        dicts = json.load(json_file)
                

    try:

            
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
            customer_email=user_email,
            metadata={'product_name': product_name},
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


    neworder = Order()
    neworder.user = user
    neworder.date_created = datetime.datetime.now()
    neworder.transaction_id = checkout_session["id"]
    neworder.url = url_data
    neworder.item_description = name
    neworder.revisions_data = revisions_data
    neworder.save()


    print(checkout_session)
    session = checkout_session
    transaction_id = session["id"]
    send_mail(
        subject='Here is your product',
        message='Thanks for your purchase',
        recipient_list=[user_email],
        from_email=settings.EMAIL_HOST_USER
    )

    send_mail(
        subject='You have a new order!',
        message='Fill it out',
        recipient_list='luismvg41@gmail.com',
        from_email=settings.EMAIL_HOST_USER
    )
    
    if json_data != 'json_data4.json':
        os.remove(json_data)
    else:
        send_mail(
        subject='Activate the script!',
        message='Activate the script!',
        recipient_list='luismvg41@gmail.com',
        from_email=settings.EMAIL_HOST_USER
    )
    
def my_dashboard(request):
    return render(request, 'user/dashboard.html')


def order_list(request):
    try:
        orders = Order.objects.filter(user=request.user).order_by('-id')
    except:
        orders = None
    if request.method =='POST':

        id_data = request.POST['order_id']
        order_data1 = Order.objects.get(id=int(id_data))  
        new_description = request.POST['update_data'] 
        old_desc = order_data1.item_description 

        if old_desc != new_description: 
            revision_data = request.POST['order_revision']
            order_data1.revisions_data = (int(order_data1.revisions_data) -1)
            order_data1.item_description = new_description
            order_data1.license_file = None
            order_data1.complete = 'In Progress'
            order_data1.save()



    return render(request, 'user/order_list.html',{'orders':orders})
        

def description_check_regular(request):
    if request.method =='POST':
        global name
        global price0
        name = request.POST['searchTxt']
        variable = {'name':name,
                    'price':price0,
                    }
    return render(request, 'description_check_regular.html',variable)
def description_check_pro(request):
    if request.method =='POST':
        global name
        global price1
        name = request.POST['searchTxt2']
        variable = {'name':name,
                    'price':price1,
                    }  
   
    return render(request, 'description_check_pro.html',variable)
def description_check_platinum(request):
    if request.method =='POST':
        global name
        global price2
        name = request.POST['searchTxt3']
        variable = {'name':name,
                    'price':price2,
                    }        
    return render(request, 'description_check_platinum.html',variable)
