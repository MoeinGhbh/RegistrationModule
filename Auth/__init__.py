from flask import Flask
from Auth.models import CreateTable,Connection
import os
import config


app = Flask(__name__)

db_name = config.database_name['path'] 
PATH = os.path.join(os.path.dirname(__file__), f'../{db_name}')
MyConnection= Connection()
MyConnection._path=PATH

CreateTable().create_table(MyConnection)


from Auth import routs

