from django.urls import path, re_path

from . import views
from .views import ItemDetailView

app_name = 'items'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    re_path(r'^(?P<Category>[\w-]+)/$', ItemDetailView.as_view(), name='details'),

]