from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.core.mail import send_mail
from django.conf import settings
from celery.result import AsyncResult
from .models import Product, Order
from .forms import NameForm
import stripe
import json
import os
import random
import datetime


# Define the product pricing and product IDs
PRODUCTS_STRIPE_PRICING_ID = {
    'product_regular': 'price_1MvNFaIQDkGdDbUY0KU0Gm4e',
    'product_pro': 'price_1MvNGFIQDkGdDbUYqGx8czJ5',
    'product_platinum': 'price_1MvNFwIQDkGdDbUYJHQr0HSW',
}

PRODUCTS_STRIPE_PRODUCTS_ID = {
    'product_regular': 'prod_1MvND7IQDkGdDbUY84rByU6F',
    'product_pro': 'prod_1MvNEzIQDkGdDbUYz9f5bzli',
    'product_platinum': 'prod_1MvNFJIQDkGdDbUYRl0pZ9XN',
}


def home(request):
    """
    Home page view.
    """
    try:
        user_email = request.user.email
        user = request.user
    except:
        pass

    # Load pricing data from JSON file
    json_data = None
    for i in range(5):
        try:
            json_data = f'json_data{i}.json'
            with open(json_data, encoding='utf-8') as json_file:
                dicts = json.load(json_file)
                break
        except:
            continue

    # Set pricing variables
    price0 = dicts['price0']
    price1 = dicts['price1']
    price2 = dicts['price2']
    url_data = dicts['url']
    revisions_data = dicts['revisions']
    variable = {
      'type0':dicts['type0'],
      'price0':dicts['price0'],
      'full_price0':dicts['full_price0'],
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
      'full_price1':dicts['full_price1'],
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
      'full_price2':dicts['full_price2'],
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

# Define the success view
def success(request):
    return render(request, 'orders/success.html')

# Define the cancel view
def cancel(request):
    return render(request, 'orders/cancel.html')


# Define the Stripe Pricing ID for each product
PRODUCTS_STRIPE_PRICING_ID = {
    'product_regular': 'price_1MvNFaIQDkGdDbUY0KU0Gm4e',
    'product_pro': 'price_1MvNGFIQDkGdDbUYqGx8czJ5',
    'product_platinum': 'price_1MvNFwIQDkGdDbUYJHQr0HSW',
}

# Define the Stripe Products ID for each product
PRODUCTS_STRIPE_PRODUCTS_ID = {
    'product_regular': 'prod_NgklgdcS9FRdq2',
    'product_pro': 'prod_NgklZip6JvzoXq',
    'product_platinum': 'prod_NgklsIdd0RGlCD',
}


# Define the view that creates a Stripe checkout session
@login_required
@csrf_exempt
def create_stripe_checkout_session(request, product_name):
    i = 0
    while True:
        try:
            with open(f'json_data{i}.json', encoding='utf-8') as json_file:
                dicts = json.load(json_file)
            break
        except:
            i += 1
            if i == 5:
                return JsonResponse({'error': 'Failed to read json data'})

    # Retrieve the current price for the selected product
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
            'product_platinum': price2,
        }
    except Exception as e:
        return JsonResponse({'error': str(e)})

    # Create a new price for the selected product
    try:
        stripe.Price.create(
            unit_amount=PRODUCTS_STRIPE_NOW_PRICE[product_name],
            currency="eur",
            product=PRODUCTS_STRIPE_PRODUCTS_ID[product_name],
        )

        # Get the latest price data
        prices = stripe.Price.list(limit=1)
        price = prices['data'][0]

        # Create the checkout session
        user_email = request.user.email
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=user_email,
            metadata={'product_name': product_name},
            line_items=[
                {'price': price['id'], 
                 'quantity': 1},
            ],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )
        
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
    
# Endpoint to handle Stripe webhook events for completed sessions with paid status
@require_POST
@csrf_exempt
def stripe_webhook_paid_endpoint(request):
    # Get the payload and Stripe signature from the request
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', None)
    event = None

    # Verify the signature and create a local instance of the event
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_SIGNING_SECRET)
    except ValueError:
        # Invalid payload
        return HttpResponseBadRequest()
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponseBadRequest()

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        # Make sure it's already paid and not delayed
        if checkout_session.payment_status == 'paid':
            _handle_successful_payment(checkout_session)

    # Passed signature verification
    return HttpResponse(status=200)


# Function to handle successful payment for a checkout session
def _handle_successful_payment(checkout_session):
    # Define what to do after the user has successfully paid

    user_email = checkout_session['customer_details']['email']
    url_data = checkout_session['metadata']['url']
    revisions_data = checkout_session['metadata']['revisions_data']
    json_data = checkout_session['metadata']['json_data']
    name = checkout_session['metadata']['name']
    user_id = checkout_session['customer']
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        user = None

    new_order = Order()
    new_order.user = user
    new_order.date_created = datetime.datetime.now()
    new_order.transaction_id = checkout_session['id']
    new_order.url = url_data
    new_order.item_description = name
    new_order.revisions_data = revisions_data
    new_order.save()

    # Send email to customer with product information and progress link
    send_mail(
        subject='Here is your product',
        message='Thanks for your purchase, to check the progress of your product go to https://www.troviders.com/orders/',
        recipient_list=[user_email],
        from_email=settings.EMAIL_HOST_USER
    )

    # Send email to business to notify of new order
    send_mail(
        subject='You have a new order!',
        message='Fill it out',
        recipient_list='luismvg41@gmail.com',
        from_email=settings.EMAIL_HOST_USER
    )

    # Remove uploaded file if it exists and it's not the default data file
    if json_data != 'json_data4.json':
        os.remove(json_data)
    else:
        # Send email to business to request more data if the default data file was uploaded
        send_mail(
            subject='More data needed',
            message='More data needed',
            recipient_list='luismvg41@gmail.com',
            from_email=settings.EMAIL_HOST_USER
        )


# View function for user dashboard
def my_dashboard(request):
    return render(request, 'user/dashboard.html')

# Function to display a list of orders for the logged-in user, and update order description if requested.
def order_list(request):
    try:
        # Get all orders for the current user and sort them by ID in descending order.
        orders = Order.objects.filter(user=request.user).order_by('-id')
    except:
        orders = None
    
    # If a POST request is received (i.e., a user has submitted a form), update the order description.
    if request.method =='POST':
        # Get the ID of the order to update and the new description from the form data.
        id_data = request.POST['order_id']
        order_data1 = Order.objects.get(id=int(id_data))  
        new_description = request.POST['update_data'] 
        
        # Check if the new description is different from the existing description.
        old_desc = order_data1.item_description 
        if old_desc != new_description: 
            # If there is a change, update the order with the new description and mark it as "In Progress".
            revision_data = request.POST['order_revision']
            order_data1.revisions_data = (int(order_data1.revisions_data) -1)
            order_data1.item_description = new_description
            order_data1.license_file = None
            order_data1.complete = 'In Progress'
            order_data1.save()

    # Render the HTML template with the order data.
    return render(request, 'dashboard/order_list.html',{'orders':orders})
        

# Function to display the "regular" subscription plan search page.
def description_check_regular(request):
    if request.method =='POST':
        # Get the search query from the form data and store it in a global variable.
        global name
        global price0
        name = request.POST['searchTxt']
        variable = {'name':name,
                    'price':price0,
                    }
    # Render the HTML template with the search results (if any).
    return render(request, 'description_check_regular.html',variable)

# Function to display the "pro" subscription plan search page.
def description_check_pro(request):
    if request.method =='POST':
        # Get the search query from the form data and store it in a global variable.
        global name
        global price1
        name = request.POST['searchTxt2']
        variable = {'name':name,
                    'price':price1,
                    }  
   
    # Render the HTML template with the search results (if any).
    return render(request, 'description_check_pro.html',variable)

# Function to display the "platinum" subscription plan search page.
def description_check_platinum(request):
    if request.method =='POST':
        # Get the search query from the form data and store it in a global variable.
        global name
        global price2
        name = request.POST['searchTxt3']
        variable = {'name':name,
                    'price':price2,
                    }        
    # Render the HTML template with the search results (if any).
    return render(request, 'description_check_platinum.html',variable)