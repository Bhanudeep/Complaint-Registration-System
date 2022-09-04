from flask import Flask, request, render_template , Response,url_for
import math, random,smtplib
from datetime import datetime
import pymongo
import json
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mylib"]
mycol = mydb["matter"]
mycol1 = mydb["users"]
mycol2 = mydb["valid"]
app = Flask(__name__)  
def mail():
   string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
   OTP = ""
   length = len(string)
   for i in range(6) :
      OTP += string[math.floor(random.random() * length)]
   now = datetime.now()
   time=str(now.strftime("%I:%M %p"))
   content = '\nHello, otp for verification is '+OTP 
   username = "8888888888"
   password = "********"
   sender = "ACRA"
   recipient = "sathvickganesh54@gmail.com"
   mail = smtplib.SMTP("smtp.gmail.com",587)
   mail.ehlo() 
   mail.starttls() 
   mail.ehlo()
   mail.login(username,password)
   header = 'To:' + recipient + '\n' + 'From:' + sender + '\n' + 'Subject: Verification code \n'
   content = header+content
   mail.sendmail(sender,recipient,content)
   mail.close
@app.route('/', methods =["GET", "POST"])
def index():
   return render_template("main.html")

@app.route('/autlog')
def autlog():
   if request.method == 'POST':
      return redirect(url_for('main'))
   return render_template('autlog.html')

@app.route('/log')
def log():
   if request.method == 'POST':
      return redirect(url_for('main'))
   return render_template('login.html')

@app.route('/loginfu', methods =["GET", "POST"])
def loginfu():
   if request.method == 'POST':
      username = request.form.get("f")
      password = request.form.get("d")
      loginfu.var=username
      users={"username":username,"password":password}
      mycol1.insert_one(users)
   return render_template('home.html')

@app.route('/logoutfu')
def logoutfu():
   if request.method == 'POST':
      return redirect(url_for('logout.html'))
   return render_template('login.html')

@app.route('/signin', methods =["GET", "POST"])
def signin():
   global k
   if request.method == 'POST':
      username = request.form.get("f")
      password = request.form.get("d")
      valid={"username":username,"password":password}
      mycol2.insert_one(valid)
   return render_template('signup.html')

@app.route('/goback')
def goback():
   if request.method == 'POST':
      return redirect(url_for('signup'))
   return render_template('main.html')

@app.route('/report')
def report():
   mail()
   if request.method == 'POST':
      return redirect(url_for('autlog'))
   return render_template('report.html')

@app.route('/crime')
def crime():
   if request.method == 'POST':
      return redirect(url_for('report'))
   return render_template('crime.html')

@app.route('/submit', methods =["GET", "POST"])
def submit():
   if request.method == "POST":
      content = request.form.get("content")
      print(content)
      matter={"crime report":content,"username":loginfu.var}
      mycol.insert_one(matter)
   return render_template("home.html")

@app.route('/gg')
def gg():
   res=""
   bad_chars = [ '"', '{', "}",","]
   for x in mycol.find({},{ "_id": 0, "crime report": 1, "username": 1 }):
      print(x)
      result=json.dumps(x)
      res=res+"\n"+result
      for i in bad_chars :
         res = res.replace(i, '')
   if request.method == 'POST':
      return redirect(url_for('crime'))
   return render_template('crime.html',mes=res)

if __name__=='__main__':
   app.run(host="192.168.29.153",port="8000",use_reloader=True,debug=True)
