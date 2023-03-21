from django.urls import path
from mainlobby import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('success/', views.success,name='success'),
    path('cancel/', views.cancel,name='cancel'),
    path('checkout/', views.checkout, name='checkout'),
]