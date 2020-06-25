from flask import Flask
from Auth.models import CreateTable,Connection

app = Flask(__name__)


connect= Connection()
con=connect.sql_connection()
crt_table= CreateTable()
crt_table.Create_table(con)


from Auth import routs

