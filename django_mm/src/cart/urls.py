from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_home, name='cart_home'),
    path('update/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout_home, name='checkout')
]
