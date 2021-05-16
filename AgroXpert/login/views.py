from django.shortcuts import render
import mysql.connector as sql
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password,check_password
import base64
# Create your views here.
login_failed=False
def expertchat(request):
    reply=''
    qn=""
    if request.session.get('FID',None) is None:
        return render(request,'farmer.html',{"res": "Please Login again Session expired ", "failed": True})
    fid=request.session['FID']
    s_query="SELECT  * from chats where FID= %s   "
    response=[]
    try:
        conn = sql.connect(host="localhost",
                           user="root",
                           password="",
                           database="agroxpert")
        cur=conn.cursor()
        cur.execute(s_query,(fid,))
        result=cur.fetchall()
        for chat in result:
            if chat[1] is not None:
                response.append((chat[3],chat[4],chat[5]))
            else:
                response.append((chat[3],chat[4],"Please wait for reply by expert"))
        print(response)
    except Exception as ex:
        response = str(ex)
        print(response)
    return (render(request,"expertchat.html",{"response":response}))
def chat(request):
    Reply="none"
    query=""
    if request.session.get('FID', None) is not None:
        fid = request.session['FID']
        fids=(fid,)
        Reply="inside session"
        sqlq="SELECT * from chats where FID=%s"
        try:
            conn = sql.connect(host="localhost",
                               user="root",
                               password="",
                               database="agroxpert")
            cur = conn.cursor()
            cur.execute(sqlq,fids)
            result=cur.fetchall()
            Reply=result
            cur.close()
            request = request.POST
            print(result)
            if len(result)<1 or result[len(result)-1][4] is None:
                curs=conn.cursor()
                print(request)
                sqli="INSERT into chats (FID, subject ,chat) values (%s,%s ,%s)"
                curs.execute(sqli,(fid,request['sub'],request['Search']))
                conn.commit()
            else:
                sqli="INSERT into chats (AID, FID, subject,chat, checked) values (%s, %s, %s, %s, %s)"
                insert_cursor=conn.cursor()
                insert_cursor.execute(sqli,(result[len(result)-1][1],fid,request['sub'],request['Search'],True))
                conn.commit()
        except Exception as ex:
            Reply=str(ex)
        conn.commit()
        conn.close()
    return JsonResponse({"query":request['Search'],"Reply":Reply})
def farmerChatbot(request):
    #FID=request.session['FID']
    if request.session.get('FID', None) is None:
        return HttpResponseRedirect('home')
    return render(request,'chatbot.html')
def home(request):
    if request.session.get('FID', None) is not None:
        del request.session['FID']
        return HttpResponseRedirect('home')
    if request.session.get('AID', None) is not None:
        del request.session['AID']
        return HttpResponseRedirect('home')
    return render(request,'home.html')
def admin(request):
    return render(request,'admin.html')
def farmer(request):
    return render(request,'farmer.html')
def farmerlogin(request):
    res = ""
    password=True
    login_failed=False
    if request.method=="POST":
        print()
        try:
            conn = sql.connect(host="localhost",user="root",password="",database="agroxpert")
            cur = conn.cursor()
            print(True)
        except Exception as ex:
            print(False)
            return render(request,"farmer.html",{"res":"Connection is not available"})
        met=request.POST
        fid = met['fid']
        pas = met['pas']
        sample_string_bytes = pas.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        password = base64_bytes.decode("ascii")
        inp = (fid,password)
        sqlq = 'SELECT * from farmer where FID=%s and pas=%s'
        cur.execute(sqlq, inp)
        fetchRes = cur.fetchall()
        if len(fetchRes)==1:
            request.session['FID']=fid
            login_failed = False
            return HttpResponseRedirect('farmer')
        else:
            login_failed=True
            res = "Unable to Signin Password or farmer Id entered is incorrect"
            print(res,fetchRes)
        conn.commit()
        conn.close()
    return render(request, 'farmer.html', {"res": res, "failed": login_failed})
def farmers(request):
    return HttpResponseRedirect('/farmerLogin')
def adminstrations(request):
    return HttpResponseRedirect('/adminLogin')
def farmerRegister(request):
    res = ""
    if request.method == "POST":
        try:
            conn=sql.connect(host="localhost",
                user="root",
                password="",
                database="agroxpert")
            cur = conn.cursor()
            print(True)
        except Exception as ex:
            print(False)
        met = request.POST
        fid=met['fid']
        fname=met['fname']
        pas=met['pas']
        phone=met['phone']
        sample_string_bytes = pas.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        password = base64_bytes.decode("ascii")
        cur.execute('insert into farmer values(%s, %s, %s, %s)',(fid,fname,phone,password))
        conn.commit()
        conn.close()
        request.session['FID'] = fid
        return HttpResponseRedirect('farmerLogin')
    return render(request,'farmer.html')
def signin(request):
    res=""
    login_failed = False
    conn = sql.connect(host="localhost",user="root",password="",database="agroxpert")
    cur = conn.cursor()
    if request.method=="POST":
        password=True
        met=request.POST
        aid=met['aid']
        pas=met['pas']
        sample_string_bytes = pas.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        password = base64_bytes.decode("ascii")
        inp=(aid,password)
        sqlq = 'SELECT * from admin where AID=%s and pas=%s'
        cur.execute(sqlq,inp)
        fetchRes = cur.fetchall()
        if len(fetchRes) == 1:
            request.session['AID']=aid
            login_failed = False
            conn.commit()
            conn.close()
            return HttpResponseRedirect('administration/')
        else:
            login_failed = True
            res = "Unable to Signin Password or Admin Id entered is incorrect"
            print(res)
    return render(request,'admin.html',{"res":res,"failed":login_failed})
def signup(request):
    res = ""
    conn = sql.connect(host="localhost",user="root",password="",database="agroxpert")
    try:
        cur=conn.cursor()
        print(True)
    except Exception as ex:
        print(ex)
    if request.method == "POST":
        met = request.POST
        aid = met['aid']
        email=met['email']
        pas = met['pas']
        name=met['name']
        sample_string_bytes = pas.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        password = base64_bytes.decode("ascii")
        inp = (aid,name,email,password)
        cur.execute('insert into admin values(%s,%s,%s,%s)', inp)
        conn.commit()
        conn.close()
        return HttpResponseRedirect('/adminLogin')
    return render(request,'admin.html')
