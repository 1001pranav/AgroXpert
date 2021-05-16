from django.urls import path,include
from  chatbot.views import *
urlpatterns=[

    path("",Home,name='Home'),
    path("addQuestions",AddQuestion,name='addQuestion'),
    path('administration/',administrator),
    path('farmer/chatbot',Chatbot,name='Chatbot'),
    path('showQuestion',ShowQuestion,name='EditQuestion'),
    path('editQuestion',EditQuestion,name='EditQuestion'),
    path('checkMail',checkMail,name='EditQuestion'),
    path('Mail',Mail,name='EditQuestion'),
]