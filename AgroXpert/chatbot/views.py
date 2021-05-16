from django.http import JsonResponse
from django.http import HttpResponseRedirect
import mysql.connector as sql
import csv
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
    for item in csv.reader(data):
        trainer.train(item)
# Create your views here.
train()
from django.shortcuts import render
def display():
    data = open(file_path)
    qna = []
    for item in csv.reader(data):
        qna.append(item)
    return qna
# Create your views here.
def Mail(request):
    if request.session.get('AID',None) is None:
        return render(request,"admin.html",{"res":"Please Login again, Error in Login","failed":True})
    aid=request.session['AID']
    response=request.POST
    try:
        conn=sql.connect(host="localhost",user="root",password="",database="agroxpert")
        cur = conn.cursor()
        query="UPDATE chats set AID=%s, Reply = %s, checked=%s WHERE CID=%s"
        cur.execute(query,(aid, response['reply'],True,response['cid']))
        conn.commit()
        conn.close()
    except Exception as ex:
        return render(request, "admin.html", {"res": ex,"failed":True})
    return render(request,'administrator.html')
def checkMail(request):
    if request.session.get('AID',None) is None:
        return render(request,"admin.html",{"res":"Please Login again, Error in Login","failed":True})
    aid=request.session['AID']
    response=[]
    try:
        conn=sql.connect(host="localhost",user="root",password="",database="agroxpert")
        cur = conn.cursor()
        query="SELECT * from chats WHERE AID=%s or checked IS NULL or AID IS NULL"
        cur.execute(query,(aid,))
        mails=cur.fetchall()
        for chat in mails:
            if chat[6] is not None :
                response.append((chat[3],chat[4],chat[5],chat[0]))
            else:
                response.append((chat[3],chat[4],"-a",chat[0]))
    except Exception as ex:
        conn.close()
        return render(request, "admin.html", {"res": ex,"failed":True})
    conn.close()
    return render(request,'administrator.html',{"response":response,"mail":True})
def administrator(request):
    qna=display()
    return render(request,'administrator.html')
def farmerChatbot(request):
    return render(request,'chatbot.html')
def Home(request):
    print(request,"i")
    if request.method=='GET':
        qna=display()
        return render(request, 'administrator.html', {"qna": qna})
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
    if request.session.get('AID',None) is None:
        return render(request,"admin.html",{"res":"Please Login again, Error in Login","failed":True})
    if request.method=='POST':
        global file_path
        data_file = open(file_path, "a")
        method=request.POST
        qns=method["question"]
        ans=method["answer"]
        urls=method['url']
        link=False
        if "," in urls:
            urls=urls.split(",")
        else:
            urls=[urls,]
        link_count=1
        link=""
        for url in urls:
            link +=" <a href='"+url+"'> Link "+str(link_count)+"click me</a>"
            link_count +=1
        ans +=link
        QnA_data=str("\""+qns+"\""+","+"\""+ans+"\"\n")
        data_file.write(QnA_data)
        data_file.close()
        csvfile=open(file_path)
        for datas in csv.reader(csvfile):
            trainer.train(datas)
        csvfile.close()
    return(render(request,'administrator.html'))
def ShowQuestion(request):
    if request.session.get('AID',None) is None:
        return render(request,"admin.html",{"res":"Please Login again, Error in Login","failed":True})
    data_file=open(file_path)
    dataset=[]
    for row in csv.reader(data_file):
        dataset.append(row)
    return render(request,'administrator.html',{"dataset":dataset})
def EditQuestion(request):
    if request.session.get('AID',None) is None:
        return render(request,"admin.html",{"res":"Please Login again, Error in Login","failed":True})
    chatbots.storage.drop()
    data_file = open(file_path,"r")
    method=request.POST
    print(method['button'])
    if request.method=="POST":
        if method['button']=='Edit':
            readLine=data_file.readlines()
            qna="\""+method['qn']+"\",\""+method['ans']+"\",\n"
            readLine[int(method['id'])]=qna
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
        datasets=open(file_path)
        for item in csv.reader(datasets):
            trainer.train(item)
        data.close()
    data_file.close()
    return HttpResponseRedirect('/administration/')