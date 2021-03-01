from django.urls import path

from . import views

app_name = 'items'

urlpatterns = [
    path('items_list/', views.item_list, name='item_list'),
    path('details/<int:item_id>/', views.details, name='details')
]