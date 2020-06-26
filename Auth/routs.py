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
   
    HP = HashPassword()
    password =  HP.hash_password(password)
    newUser= add_user(email,password)
    newUser.insert_value()
    SendEmail(email)
    return  'user registered successfully'

@app.route('/login')
def login_form():
    return 'user logined successfully'