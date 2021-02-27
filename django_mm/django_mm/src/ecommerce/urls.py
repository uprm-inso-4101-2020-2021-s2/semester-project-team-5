"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings            # eliminate on app deployment
from django.conf.urls.static import static  # eliminate on app deployment
from .views import home_page, login_page, register_page
from items.views import ItemListView, item_list_view, ItemDetailView, item_detail_view


urlpatterns = [
    url(r'^$', home_page),
    url(r'login/$', login_page),
    url(r'register/$', register_page),
    url(r'admin/', admin.site.urls),
    url(r'items/$', ItemListView.as_view()),
    url(r'items_t/$', item_list_view),
    url(r'items/(?P<pk>\d+)/$', ItemDetailView.as_view()),
    url(r'items_t/(?P<pk>\d+)/$', item_detail_view)
]
# eliminate on app deployment
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
