from django.urls import path
from mainlobby import views
from .views import *
from .models import Order
from django_downloadview import ObjectDownloadView
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('success/', views.success,name='success'),
    path('cancel/', views.cancel,name='cancel'),
    path('create-checkout-session/<str:product_name>', create_stripe_checkout_session),
    path('stripe-webhook-paid/', stripe_webhook_paid_endpoint),
    #User
    path('dashboard/',views.my_dashboard,name='dashboard'),
    path('orders/',views.order_list,name='orders'),
    path('description_check_regular/', views.description_check_regular,name='description_check_regular'),
    path('description_check_pro/', views.description_check_pro,name='description_check_pro'),
    path('description_check_platinum/', views.description_check_platinum,name='description_check_platinum'),
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)