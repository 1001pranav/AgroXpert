from django.shortcuts import render
import mysql.connector as sql

# Create your views here.
def farmerlogin(request):
    res = ""
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
        inp = (fid, pas)
        sqlq='SELECT * from farmer where FID=%s and pas =%s'
        cur.execute(sqlq,inp)
        fetchRes=cur.fetchall()
        print(fetchRes)
        if len(fetchRes) == 1:
            return render(request, 'chatbot.html')

        else:
            res = "Unable to Signin Password or farmer Id entered is incorrect"
        conn.commit()
        conn.close()
    return render(request,'farmer.html',{"res": res})
def admin(request):
    return render(request,'admin.html')
def farmer(request):
    return render(request,'farmer.html')
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
        cur.execute('insert into farmer values(%s, %s, %s, %s)',(fid,fname,phone,pas))

        conn.commit()
        conn.close()
        return render(request, 'chatbot.html')

    return render(request,'farmer.html')
def signin(request):
    res=""
    conn = sql.connect(host="localhost",user="root",password="",database="agroxpert")
    cur = conn.cursor()
    if request.method=="POST":
        met=request.POST
        aid=met['aid']
        pas=met['pas']
        inp=(aid,pas)
        cur.execute('''SELECT * from admin where AID=%s and pas=%s''',inp)
        fetch=cur.fetchall()
        if len(fetch)==1:
            print(fetch)
            conn.commit()
            conn.close()
            return render(request,'chatbot.html')
        else:
            res = "Unable to Signin Password or Admin Id entered is incorrect"

    return render(request,'admin.html',{"res":res})
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
        inp = (aid,name,email,pas)
        cur.execute('insert into admin values(%s,%s,%s,%s)', inp)

        conn.commit()
        conn.close()
        return render(request, 'chatbot.html')
    return render(request,'admin.html')
