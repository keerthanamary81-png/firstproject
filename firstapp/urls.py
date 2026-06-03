from django.contrib import admin
from django.urls import path

from firstapp.views import login_func, predict_page,register_func,homepage_view,logout_user

urlpatterns = [
    path('',login_func,name='login_func'),
    path('register',register_func,name='register_func'),
    path('home',homepage_view,name='homepage_view'),
    path('logout',logout_user,name='logout_user'),
    path('predict', predict_page, name='predict_page'),
]
