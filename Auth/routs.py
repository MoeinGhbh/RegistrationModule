from flask import render_template,request
from Auth import app
from Auth.models import add_user
from Auth.sendEmail import SendEmail

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register_form():
    request_data = request.get_json()
    email = str(request_data["email"])
    password = str(request_data["password"])
    add_user(email,password)
    SendEmail(email)
    return render_template('register.html')

@app.route('/login')
def login_form():
    return render_template('login.html')