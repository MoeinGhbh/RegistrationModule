from sqlite3 import Error
import sqlite3
import os

class Connection():
    # create a default path to connect to and create (if necessary) a database
    # called 'database.sqlite3' in the same directory as this script
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'albeton.sqlite3')
    print(DEFAULT_PATH)
    def sql_connection(self,db_path=DEFAULT_PATH):
        try:
            con = sqlite3.connect(db_path)
            return con
        except Error:
            print(Error)
   
class CreateTable():
    def Create_table(self,con):
        cursorObj = con.cursor()
        cursorObj.execute("CREATE TABLE if not exists users(id INTEGER PRIMARY KEY, email string(30), password string(15), active int, Lock int)")
        con.commit()

class add_user():
    def __init__(self,email,password):
        self.email=email
        self.password=password
        
    def insert_value(self,con):
        # Insert a row of data
        try:
            con.execute(f'INSERT INTO users  (email,password,active,lock)' + \
                                f'VALUES ({self.email},{self.password},0,0)')
            return True
        except Error:
            return Error
        # # Save (commit) the changes
        con.commit()

class user_update():
    pass

class user_delete():
    pass

class Close():
    def close_connection(self,con):
        # # We can also close the connection if we are done with it.
        # # Just be sure any changes have been committed or they will be lost.
        con.close()