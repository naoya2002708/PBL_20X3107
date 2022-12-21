import re
from flask import Flask, render_template, request,redirect,session,make_response
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
import MySQLdb
import html
import datetime
from dicttoxml import dicttoxml

from datetime import timedelta
import secrets





def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        password="Naoya0781",
        db="user",
        use_unicode=True,
        charset="utf8")
    return con

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=60)

@app.route("/")
def rooturl():
    return redirect("login")

@app.route("/make", methods=["GET","POST"])
def make():
    if request.method == "GET":
        return render_template("make.html")
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        age = request.form["age"]
        sex = request.form["sex"]
        height = request.form["height"]
        weight = request.form["weight"]
        hashpass = gph(password)
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT * FROM user_data WHERE email=%(email)s
                    """,{"email":email})
        data=[]
        for row in cur:
            data.append(row)
        if len(data)!=0:
            return render_template("make.html", msg="既に存在するメールアドレスです")
        con.commit()
        con.close()
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO user_data
                    (name,height,weight,sex,age,email,password)
                    VALUES (%(name)s,%(height)s,%(weight)s,%(sex)s,%(age)s,%(email)s,%(hashpass)s)
                    """,{"name":name,"height":height,"weight":weight,"sex":sex,"age":age,"email":email,"hashpass":hashpass})
        con.commit()
        con.close()
        return render_template("info.html", name=name,email=email,password=password,age=age,sex=sex,height=height,weight=weight)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        print("get login")
        session.clear()
        return render_template("login.html")
    elif request.method == "POST":
        print("post login")
        email = request.form["email"]
        password = request.form["password"]
        con = connect()
        cur =con.cursor()
        cur.execute("""
                    SELECT password,name,email,age,sex,height,weight
                    FROM user_data
                    WHERE email= %(email)s
                    """,{"email":email})
        data=[]
        for row in cur:
            print("for cur")
            data.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6]])
        if len(data)==0:
            con.close()
            return render_template("login.html", msg="IDが間違っています")
        if cph(data[0][0],password):
            session["name"]=data[0][1]
            session["email"]=data[0][2]
            session["age"]=data[0][3]
            session["sex"]=data[0][4]
            session["height"]=data[0][5]
            session["weight"]=data[0][6]
            
            con.close()
            return redirect("home")
        else:
            con.close()
            return render_template("login.html",msg="パスワードが間違っています")

@app.route("/home")
def home():
    if "name" in session:
        name=session["name"]
        con=connect()
        cur=con.cursor()
        cur.execute("""
                    SELECT SUM(steps) FROM record WHERE name=%(name)s
                    """,{"name":name})
        data=[]
        for row in cur:
            data.append(row)
        
        print(data[0])
        data = [str(i) for i in data]
        dt_str = ",".join(data)
        total = re.sub("\\D", "",dt_str )
        print("total=",total)
        if len(total)==0:
            
            session["total"]="0"
        else:
            print(total)
            session["total"]=total

        #今日の歩数追加分   
        today=datetime.date.today()
        print(today)
        con=connect()
        cur=con.cursor()
        cur.execute("""
                    SELECT SUM(steps) FROM record WHERE name=%(name)s AND record_date=%(record_date)s
                    """,{"name":name,"record_date":today})
        data=[]
        for row in cur:
            data.append(row)
        
        
        data = [str(i) for i in data]
        dt_str = ",".join(data)
        today_record = re.sub("\\D", "",dt_str )
        
        if len(today_record)==0:
            print("today=",len(today_record))
            session["today_record"]=0
        else:
            print(today_record)
            session["today_record"]=today_record
            
        
        #カロリー消費量計算
        
        if session["today_record"]==0:
            session["today_calorie"]=0
        else:
            height=session["height"]
            weight=session["weight"]
            kyou=float(today_record)
            hohaba=height*0.4
            hokoukyori=hohaba*kyou/100
            print(hokoukyori)
            hokouzikann=(hokoukyori/67)
            print(hokouzikann)
            Ex=hokouzikann/60*3.0
            calorie=1.05*Ex*weight
            session["today_calorie"]=round(calorie,2)
            


        con.commit()
        con.close()
        return render_template("mypage.html",
                                total=session["total"],
                                name=html.escape(session["name"]),
                                today_calorie=session["today_calorie"],
                                today_record=session["today_record"])
                     
    else:
        return redirect("login")

    




@app.route("/record",methods=["GET","POST"])
def record():
    if "name" in session:
        if request.method == "GET":
            return render_template("record.html")
        elif request.method == "POST":
            
            name =session["name"]
            email = session["email"]
            age = session["age"]
            sex = session["sex"]
            height = session["height"]
            weight = session["weight"]
            record_date = request.form["record_date"]
            steps = request.form["steps"]
            memo = request.form["memo"]
            if len(steps)==0:
                calorie=0
            else:
                height=session["height"]
                weight=session["weight"]
                kyou=float(steps)
                hohaba=height*0.4
                hokoukyori=hohaba*kyou/100
                print(hokoukyori)
                hokouzikann=(hokoukyori/67)
                print(hokouzikann)
                Ex=hokouzikann/60*3.0
                calorie=1.05*Ex*weight
                calorie=round(calorie,2)
            
            #総歩数
            name=session["name"]
            con=connect()
            cur=con.cursor()
            cur.execute("""
                        SELECT SUM(steps) FROM record WHERE name=%(name)s
                        """,{"name":name})
            data=[]
            for row in cur:
                data.append(row)
            
            print(data[0])
            data = [str(i) for i in data]
            dt_str = ",".join(data)
            total = re.sub("\\D", "",dt_str )
            if len(total)==0:
                total=int(steps)

            else:
                total= int(total)
                total=total+int(steps)
            
        

            con = connect()
            cur = con.cursor()
            cur.execute("""
                        INSERT INTO record
                        (name,email,height,weight,sex,age,record_date,steps,memo,calorie,total)
                        VALUES (%(name)s,%(email)s,%(height)s,%(weight)s,%(sex)s,%(age)s,%(record_date)s,%(steps)s,%(memo)s,%(calorie)s,%(total)s)
                        """,{"name":name,"email":email,"height":height,"weight":weight,"sex":sex,"age":age,"record_date":record_date,"steps":steps,"memo":memo,"calorie":calorie,"total":total})
            con.commit()
            con.close()
            
            return redirect("/home")
    else:
        
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        date = html.escape(request.form["date"])
        ranking = html.escape(request.form["ranking"])
        form = html.escape(request.form["format"])

        if ranking=="steps":
            ran="歩数"
            con = connect()
            cur = con.cursor()
            cur.execute("""
            SELECT name,steps,memo
            FROM record
            WHERE record_date=%(date)s 
            ORDER BY steps DESC
            """,{"date":date})

            
        elif ranking=="calorie":
            ran="カロリー"
            con = connect()
            cur = con.cursor()
            cur.execute("""
            SELECT name,calorie,memo
            FROM record
            WHERE record_date=%(date)s
            ORDER BY calorie DESC
            """,{"date":date})



        elif ranking=="sum_steps":
            ran="今までの総歩数"
            con = connect()
            cur = con.cursor()
            cur.execute("""
            SELECT name,total,memo
            FROM record
            WHERE id IN(SELECT MAX(id) FROM record GROUP BY name)
            ORDER BY total DESC
            """,{"date":date})

            

        if form == "JSON":
            res = {}
            tmpa = []
            rank = 1
            for row in cur:
                dic = {}
                dic["rank"] = rank
                dic["name"] = row[0]
                dic["count"] = row[1]
                dic["memo"] = row[2]
                tmpa.append(dic)
                rank += 1
            res["content"] = tmpa
            con.commit()
            con.close()
            return render_template("result.html",res=res,ranking=ran)

        elif form =="XML":
            res = {}
            tmpa = {}
            dic ={}
            rank = 1
            for row in cur:
                dic['rank'+str(rank)]=rank
                dic['name'+str(rank)]= row[0]
                dic['count'+str(rank)]= row[1]
                dic['memo'+str(rank)]=row[2]
                rank +=1
            xml = dicttoxml(dic)
            resp = make_response(xml)
            resp.mimetype = "text/xml"
            con.commit()
            con.close()
            return resp


if __name__=="__main__":
    app.run(host="0.0.0.0")
