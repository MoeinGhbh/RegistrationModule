from flask import render_template,request, Response, jsonify
from Auth import app
from Auth.models import add_user,Authentication, UserUpdate
from Auth.sendEmail import SendEmail
from Auth.HashPassword import HashPassword
import datetime
from functools import wraps
import jwt


app.config["SECRET_KEY"] = 'meow'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register_form():
    # Get data from body of POST mtehod
    request_data = request.get_json()
    email = str(request_data["email"])
    password = str(request_data["password"])
    # convert password to hash format
    HP = HashPassword()
    password =  HP.hash_password(password)
    # class add user method
    newUser= add_user(email,password)
    result = newUser.insert_value()
    # if registration is successfull then send a activate e-mial
    if result:
        SendEmail(email)
    return  'user registered successfully'

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get("token")
        try:
            jwt.decode(token, app.config["SECRET_KEY"])
            return f(*args, **kwargs)
        except:
            return jsonify({"error": "Need to token to show this page"}), 401
    return wrapper

@app.route("/login", methods=["GET", "POST"])
def get_token():
    request_data = request.get_json()
    email = str(request_data["email"])
    password = str(request_data["password"])
    auth= Authentication(email,password)
    result = auth.Check_user_password()
    print(result)
    if result==True:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
        token = jwt.encode({"exp": expiration_date}, app.config["SECRET_KEY"], algorithm="HS256")
        return token
    else:
        return 'not ok ' #Response(result, mimetype='applicatio/json')


@app.route('/active')
def active_user():
    request_data = request.get_json()
    id = str(request_data["id"])
    up=UserUpdate()
    up.upser_active(id,True)
    return 'User successfully Activated'
