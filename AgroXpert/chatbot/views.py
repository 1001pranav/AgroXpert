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
data = open(file_path)

chatbots = ChatBot(name='AgroXpert', read_only=True,
                   logic_adapters=[
                       {
                           'import_path': 'chatterbot.logic.BestMatch',
                           'default_response': 'I am sorry, I do not understand. I am still learning. Please contact abc@xxx.com for further assistance.',
                           'maximum_similarity_threshold': 0.5
                       }])
trainer = ListTrainer(chatbots)
def train():
    n=0
    for item in csv.reader(data):
        n +=1
        trainer.train(item)
        print(n)# Create your views here.
train()
from django.shortcuts import render

# Create your views here.
def administrator(request):
    return render(request,'administrator.html')
def farmerChatbot(request):
    return render(request,'chatbot.html')
def Home(request):
    print(request)
    if request.method=='GET':
        return render(request,'administrator.html')
    if request.method=="POST" and request.POST['check']=="Admin":
        return (AddQuestion(request))
    elif request.POST['check']=="edit":
        return ShowQuestion(request)
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
        global file_path
        data_file = open(file_path, "a+")
        method=request.POST
        qns=method["question"]
        ans=method["answer"]
        QnA_data=str("\""+qns+"\""+","+"\""+ans+"\""+"\n")
        data_file.write(QnA_data)
        for data in data_file:
            print(data)
        trainer.train([QnA_data])
    return(render(request,'administrator.html'))
def ShowQuestion(request):
    data_file=open(file_path)
    dataset=[]
    for row in csv.reader(data_file):
        dataset.append(row)
    return render(request,'administrator.html',{"dataset":dataset})
def EditQuestion(request):
    data_file = open(file_path,"r")
    method=request.POST
    print(method['button'])
    if request.method=="POST":
        if method['button']=='Edit':
            readLine=data_file.readlines()
            readLine[int(method['id'])]="\""+method['qn']+"\",\""+method['ans']+"\" \n"
            data_file = open(file_path, "w")
            data_file.writelines(readLine)
            data_file.close()
            print()
            print(method['ans'])
        elif method['button']=='Delete':
            print("success")
            readLine = data_file.readlines()
            readLine[int(method['id'])] = ""
            data_file = open(file_path, "w")
            data_file.writelines(readLine)
            data_file.close()
            data=open(file_path)
            for item in csv.reader(data):
                trainer.train(item)
            data.close()
    data_file.close()
    return render(request,'administrator.html')