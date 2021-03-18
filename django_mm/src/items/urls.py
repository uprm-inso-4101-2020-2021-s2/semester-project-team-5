from django.urls import path, re_path

from . import views
from .views import ItemDetailView, SearchItemListView


app_name = 'items'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('search/', SearchItemListView.as_view(), name='searching'),
    re_path(r'^items/(?P<Category>[\w-]+)/$', ItemDetailView.as_view(), name='details'),
    path('items/add/', views.add_item, name='add_item'),
    path('selling/', views.selling_items, name='selling_items'),
    path('category/<int:category>', views.search_item_by_category, name='search_item_by_category'),
]
