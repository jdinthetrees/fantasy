from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login_user', views.login_user),
    path('process_user', views.process_user),
    path('dashboard', views.welcome),
    path('logout', views.logout),

]