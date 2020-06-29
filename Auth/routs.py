from flask import render_template, request, Response, jsonify, flash, redirect
from Auth import app,MyConnection
from Auth.models import Connection, AddUser, Authentication, UserUpdate
from Auth.sendEmail import SendEmail
from Auth.HashPassword import HashPassword
import datetime
from functools import wraps
import jwt
import os

app.config["SECRET_KEY"] = 'f6a6ec1916a64e3294f4bf45bf183f81'
# PATH = os.path.join(os.path.dirname(__file__), '../albeton.sqlite3')
# MyConnection= Connection()
# MyConnection._path=PATH



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    # Get data from body of POST mtehod
    request_data = request.get_json()
    email = str(request_data["email"])
    password = str(request_data["password"])
    # convert password to hash format
    HP = HashPassword()
    password = HP.hash_password(password)
    # class add user method
    newUser = AddUser(email, password,0,0,0)
    result = newUser.insert_user(MyConnection)
    print(result)
    # if registration is successfull then send a activate e-mial
    if result:
        SendEmail(email)
        return 'The username was successfully registered'
    else:
        return 'The username has already been created'


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
    auth = Authentication(email, password)
    result = auth.check_user_password(MyConnection)
    print(result)
    if result == True:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
        token = jwt.encode({"exp": expiration_date},
                           app.config["SECRET_KEY"], algorithm="HS256")
        return token
    else:
        return result

@app.route('/active',methods=['GET','POST'])
def active_user():
    request_data = request.get_json()
    id = str(request_data["id"])
    up = UserUpdate('active',id,1)
    result = up.user_update(MyConnection)
    if result:
        return 'user successfully active'
    else:
        return 'Please contact to support'

@app.route('/logout')
def logout():
	flash('you logged out successfully', 'success')
	return redirect('home.html')