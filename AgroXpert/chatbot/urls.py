from django.urls import path,include
from  chatbot.views import *
urlpatterns=[
    path('/administration/',administrator),
    path("",Home,name='Home'),
    path("addQuestion",AddQuestion,name='addQuestion'),
    path('farmer/chatbot',Chatbot,name='Chatbot'),
    path('showQuestion',ShowQuestion,name='EditQuestion'),
    path('editQuestion',EditQuestion,name='EditQuestion'),


]