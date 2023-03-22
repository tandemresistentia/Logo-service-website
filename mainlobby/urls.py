from django.urls import path
from mainlobby import views
from .views import create_stripe_checkout_session,stripe_webhook_paid_endpoint
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('success/', views.success,name='success'),
    path('cancel/', views.cancel,name='cancel'),
    path('create-checkout-session/<str:product_name>', create_stripe_checkout_session),
    path('stripe-webhook-paid/', stripe_webhook_paid_endpoint),
]