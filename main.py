import re
from flask import Flask, render_template, request,redirect,session
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
import MySQLdb
import html
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
        
        return render_template("success.html",
                               name=html.escape(session["name"]),
                               email=html.escape(session["email"]))                      
    else:
        return redirect("login")

        
if __name__=="__main__":
    app.run(host="0.0.0.0")
