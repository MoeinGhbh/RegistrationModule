from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite3:///../albeton.db'
db = SQLAlchemy(app)

from Auth import routs