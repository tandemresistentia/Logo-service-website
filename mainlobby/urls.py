from django.urls import path
from mainlobby import views
from .views import *
urlpatterns = [
    path('', views.home, name='home'),
    path('success/', views.success,name='success'),
    path('cancel/', views.cancel,name='cancel'),
    path('create-checkout-session/<str:product_name>', create_stripe_checkout_session),
    path('stripe-webhook-paid/', stripe_webhook_paid_endpoint),
    #User
    path('dashboard/',views.my_dashboard,name='dashboard'),
    path('orders/',views.order_list,name='orders'),
    path('documents/<int:document_id>/', views.download, name='download'),
]