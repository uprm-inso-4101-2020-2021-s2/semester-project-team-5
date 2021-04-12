from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path("logout/", views.logout_page, name="logout"),
    path('profile/<int:user_pk>', views.user_profile_page, name='information_page'),
]