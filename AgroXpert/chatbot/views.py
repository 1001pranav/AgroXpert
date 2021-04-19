from django.http import JsonResponse
import csv
import sqlite3 as sql
import csv
conn=sql.connect('db.sqlite3')
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, "dataset.csv")
chatbots = ChatBot(name='AgroXpert', read_only=True,
                           logic_adapters=[
                               {
                                   'import_path': 'chatterbot.logic.BestMatch',
                                   'default_response': 'I am sorry, I do not understand. I am still learning. Please contact abc@xxx.com for further assistance.',
                                   'maximum_similarity_threshold': 0.5

                               }])
def train():
    n=0
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, "dataset.csv")
    data = open(file_path)
    # creating a new chatbot
    chatbots = ChatBot(name='AgroXpert', read_only=True,
                       logic_adapters=[
                           {
                               'import_path': 'chatterbot.logic.BestMatch',
                               'default_response': 'I am sorry, I do not understand. I am still learning. Please contact abc@xxx.com for further assistance.',
                               'maximum_similarity_threshold': 0.5

                           }])

    trainer = ListTrainer(chatbots)
    for item in csv.reader(data):
        n +=1
        trainer.train(item)
    print(n)
train()
# Create your views here.
from django.shortcuts import render

# Create your views here.
def Home(request):
    if request.method=="POST" and request.POST['check']=="Admin":
        return (AddQuestion(request))
    else:
        return Chatbot(request)
def Chatbot(request):
    print("req")
    Reply=""
    query=""
    response={}
    if request.method=="POST":

        query=request.POST["Search"]
        Reply=chatbots.get_response(query)
        print(query,Reply)
        data=str(Reply)
        print(type(data))
    return JsonResponse({'query':query,'Reply':data})
def AddQuestion(request):
    if request.method=='POST':
        data_file = open(file_path, "a")
        method=request.POST
        qns=method["question"]
        ans=method["answer"]
        if(',' in ans):
            ans.replace(",","\",\"")
            print(ans)
        if(',' in qns):
            qns.replace(',',"\",\"")

        QnA_data=str(qns+","+ans+"\n")
        data_file.write(QnA_data)
        train()
    return(render(request,'administrator.html'))