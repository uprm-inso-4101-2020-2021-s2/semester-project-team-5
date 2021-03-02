from django.urls import path, re_path

from . import views
from .views import ItemDetailView

app_name = 'items'

urlpatterns = [
    path('items_list/', views.item_list, name='item_list'),
    #path('details/<int:item_id>/', views.details, name='details'),
    re_path(r'^(?P<Category>[\w-]+)/$', ItemDetailView.as_view(), name='detail1'),

]