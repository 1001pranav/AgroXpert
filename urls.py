from django.urls import path,include
from  chatbot.views import *

urlpatterns=[
path('',Chatbot,name='Chatbot'),
path('chatbot',Chatbot,name='Chatbot')
]