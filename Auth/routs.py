from flask import render_template,request
from Auth import app
from Auth.models import add_user
from Auth.sendEmail import SendEmail
from Auth.HashPassword import HashPassword

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register_form():
    request_data = request.get_json()
    email = str(request_data["email"])
    
    password = str(request_data["password"])
    verify_password = str(request_data["verify-password"])
    HP = HashPassword()
    password =  HP.hash_password(password)
    verify_password =  HP.hash_password(verify_password)
    if HP.verify_password(password,verify_password):
        add_user(email,password)
    SendEmail(email)
    return render_template('register.html')

@app.route('/login')
def login_form():
    return render_template('login.html')