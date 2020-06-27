from flask import Flask
from Auth.models import CreateTable,Connection

app = Flask(__name__)
CreateTable.create_table()


from Auth import routs

