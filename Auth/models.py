from sqlite3 import Error
import sqlite3
import os

class Connection():
    # create a default path to connect to and create (if necessary) a database
    # called 'database.sqlite3' in the same directory as this script
    DEFAULT_PATH = os.path.join(os.path.dirname(__file__), '../albeton.sqlite3')
    print(DEFAULT_PATH)
    def sql_connection(self,db_path=DEFAULT_PATH):
        try:
            con = sqlite3.connect(db_path, check_same_thread=False)
            return con
        except Error:
            print(Error)
   
class CreateTable():
    def Create_table(self,con):
        cursorObj = con.cursor()
        try:
            cursorObj.execute(f'CREATE TABLE if not exists users ' + \
                              f'(id       INTEGER PRIMARY KEY,'    + \
                              f' email    string(50) UNIQUE,'      + \
                              f' password string(50) UNIQUE,'      + \
                              f' active   int,'                    + \
                              f' Lock     int)')
            return True
        except Error:
            return Error
        con.commit()

class add_user():
    connect = Connection()
    con=connect.sql_connection()

    def __init__(self,email,password):
        self.email=email
        self.password=password
        
    def insert_value(self):
        # Insert a row of data
        try:
            add_user.con.execute(f'INSERT INTO users' + \
                                 f'(email,password,active,lock)' + \
                                 f'VALUES (?,?,?,?)'
                                 ,(self.email,self.password,0,0))
            return True
        except Error:
            return Error
        # Save (commit) the changes
        add_user.con.commit()

class user_update():
    pass

class user_delete():
    pass

class Close():
    def close_connection(self,con):
        # # We can also close the connection if we are done with it.
        # # Just be sure any changes have been committed or they will be lost.
        con.close()