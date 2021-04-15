from django.urls import path,include
from  chatbot.views import *

urlpatterns=[
    path("",Home,name='Home'),
    path("addQuestion",AddQuestion,name='addQuestion'),
    path('chatbot',Chatbot,name='Chatbot'),

]