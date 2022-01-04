from flask import Flask
from flask import request, session, redirect,url_for
from flask import render_template
import Login
import basic
app= Flask(__name__,static_folder="static",static_url_path="/")
app.config['SECRET_KEY'] = 'os.urandom(24)'

@app.route("/")
def hello():
    return render_template("login.html")

@app.route("/login.html", methods=["POST","GET"])
def login():
    if request.method == "POST":
        uid     =   request.form["uid"]
        upass   =   request.form["upass"]
        status = Login.login(uid,upass)
        if status == 2:
            session['user'] = uid
            return redirect(url_for('manu'))
        else:
            return redirect(url_for('no'))
    else:    
        return render_template("login.html")

@app.route("/register.html", methods=["POST","GET"])
def register():
    if request.method == "POST":
        uid     =   request.form["uid"]
        upass   =   request.form["upass"]
        uline   =   request.form["uline"]
        status = Login.register(uid,upass,10000,uline)
        if status == 1:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('no'))
    else:    
        return render_template("register.html")

@app.route("/view.html")
def view():
    if session.get('user') == '':
        return redirect(url_for('login'))

    return render_template("view.html")

@app.route("/trans.html", methods=["POST","GET"])
def trans():
    if session.get('user') == '':
        return redirect(url_for('login'))

    if request.method == "POST":
        inid    =   request.form["inid"]
        outid   =   session.get('user')
        money   =   request.form["money"]


        status = basic.makeTransaction(inid,outid,money)
        if status == 0:
            #session['user'] = uid
            return redirect(url_for('yes'))
        elif status == 1:
            return redirect(url_for('yes'))
        else:
            return redirect(url_for('no'))
    else:    
        return render_template("trans.html")

@app.route("/manu.html")
def manu():
    if session.get('user') == '':
        return redirect(url_for('login'))

    user = basic.getUser(session.get('user'))
    return render_template("manu.html",id=user[0],money=user[2])

@app.route("/Info.html")
def Info():
    if session.get('user') == '':
        return redirect(url_for('login'))

    return render_template("Info.html")

@app.route("/fori.html")
def fori():
    if session.get('user') == '':
        return redirect(url_for('login'))

    return render_template("fori.html")

@app.route("/atm.html", methods=["POST","GET"])
def atm():
    if session.get('user') == '':
        return redirect(url_for('login'))

    if request.method == "POST":
        money   =   request.form["money"]
        uid     =   session.get('user')
        status  =   basic.makeTransaction(uid,"ATM",money)
        print(status)
        if status == 0:
            return redirect(url_for('yes'))
        elif status == 1:
            return redirect(url_for('yes'))
        else:
            return redirect(url_for('no'))
    else:    
        return render_template("atm.html")

@app.route("/fun")
def fun():
    num1 = int(request.args.get("max",100))
    num2 = int(request.args.get("min",1))
    a = 0
    for i in range(num2,num1+1):
        a += i
    return str(a)

@app.route("/linecheck", methods=["GET"])
def linecheck():
    tid = request.args.get('id')
    basic.LineCheck(tid)
    return render_template("Info.html")

@app.route("/linecancle", methods=["GET"])
def linecancle():
    tid = request.args.get('id')
    basic.LineCheck(tid)
    return render_template("Info.html")

@app.route("/no")
def no():
    return 'no'

@app.route("/yes")
def yes():
    return 'yes'



if __name__=="__main__":
    app.run(host='127.0.0.9',port=4455,debug=True) 
