from flask import Flask
from Auth.models import CreateTable,Connection
import os
import config


app = Flask(__name__)

# Get path of current file
db_name = config.database_name['path'] 
# make address of database
PATH = os.path.join(os.path.dirname(__file__), f'../{db_name}')
# instantiate object from connection class
MyConnection= Connection()
# set property of database path
MyConnection._path=PATH

# make connection and send for routs file
CreateTable().create_table(MyConnection)


from Auth import routs

