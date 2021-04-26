from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_home, name='cart_home'),
    path('update/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout_home, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:cart_id>/', views.orders_details, name='orders_details'),
    path('sells_activity/', views.sells_activity, name='sells_activity'),
]
