from django.urls import path,include
from login.views import *
from login.views import *
urlpatterns=[
    path('',home,name='home'),
    path('home',home,name='home'),
    path('farmer',farmerChatbot,name='farmer'),
    path('admin',admin,name='admin'),
    path('adminLogin',signin,name='admin'),
    path('farmerLogin',farmerlogin,name='Farmer'),
    path('farmerRegister',farmerRegister,name='admin'),
    path('signin',signin,name='signin'),
    path('signup',signup,name='signup'),
    path('farmer/Chat',expertchat),
    path('farmer/Expertchat',chat),
]