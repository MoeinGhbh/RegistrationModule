from sqlite3 import Error
import sqlite3
import os
from Auth.HashPassword import HashPassword

class Singleton(type):
    _instance = None

    def __call__(self, *args, **kwargs):
        if self._instance==None:
            self._instance= super().__call__()
        return self._instance

class Connection(metaclass=Singleton):
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
    connect= Connection()
    con=connect.sql_connection()

    @staticmethod
    def Create_table():
        cursorObj = CreateTable.con.cursor()
        try:
            cursorObj.execute(f'CREATE TABLE if not exists users ' + \
                              f'(id       INTEGER PRIMARY KEY,'    + \
                              f' email    string(100) UNIQUE,'     + \
                              f' password string(100) UNIQUE,'     + \
                              f' active   int,'                    + \
                              f' Lock     int,'                    + \
                              f' incorrectPass int )')
            return True
        except Error:
            return Error
        CreateTable.con.commit()

class add_user():
    connect = Connection()
    con=connect.sql_connection()

    def __init__(self,email,password):
        self.email=email
        self.password=password
        
    def insert_value(self):
        # Insert a row of data
        try:
            add_user.con.execute(f' INSERT INTO users ' + \
                                 f' (email,password,active,lock,incorrectPass) ' + \
                                 f' VALUES (?,?,?,?,?) '
                                 ,(self.email,self.password,0,0,0))
                                 # Save (commit) the changes
            add_user.con.commit()
            return True
        except Error:
            return Error
        
        return True

class Authentication():
    connect = Connection()
    con=connect.sql_connection()
    hp = HashPassword()

    def __init__(self,email,password):
        self.email=email
        self.password= password

    def Check_user_password(self):
        cursor = self.con.cursor()
        # select a row from data
        try:
            cursor.execute(f' select id,email,password,active,lock,incorrectPass from users where email=?'
                                 ,(self.email,))
            rows = cursor.fetchall() 
            cursor.close()

            if len(rows)>0:
                if Authentication.hp.verify_password(rows[0][1],self.password):
                    print('password is correct')
                    if len(rows)>0 :
                        
                        id = rows[0][0]
                        isactive=int(rows[0][3])
                        islock=int(rows[0][4])
                        incorrectPass=int(rows[0][5])

                        if isactive==0:
                            return 'Account is not active'
                        elif isactive==1 and islock==0:
                            return True
                        elif isactive==1 and islock==1:
                            return 'Account is Locked'
                      
                    else:
                        return 'Account is not exist'
                else:
                    id = int(rows[0][0])
                    incorrectPass=int(rows[0][5])
                    uuip= UserUpdate()
                    uuip.user_incorrectpass(id,incorrectPass)
                    print('password is not correct')

        except Error:
            return Error


class UserUpdate():
    connect = Connection()
    con=connect.sql_connection()

    def upser_active(self,id,active):
        cursor = self.con.cursor()
        # select a row from data
        # try:
            # cursor.execute(f' upadte users set active=? where id=?',(active,id))
        print(f' update users set active = 1 where id = 1 ')
        cursor.execute(f' update users set active = 1 where id = 1 ')
        # except Error:
        #     return Error
    
    def user_lock(self,id,lock):
        cursor = UserUpdate.con.cursor()
        # select a row from data
        try:
            cursor.execute(f' update users set lock = ? where id = ? ',(lock,id))
            UserUpdate.con.commit()
            cursor.close()
        except Error:
            return Error
        

    def user_incorrectpass(self,id,incorrectPass):
        cursor = UserUpdate.con.cursor()
        # select a row from data
        incorrectPass+=1
        # hhhhhhhhhhhaaaaaaaaaaaaaaaaaaaaaaarrrrrrrrrrrrrdddddddd code
        if incorrectPass>3:
            print(incorrectPass)
            ss = UserUpdate()
            ss.user_lock(id,1)
        else:
            try:
                cursor.execute(f'  UPDATE users set incorrectPass = ? where id = ? ',(incorrectPass,id))
                UserUpdate.con.commit()
                cursor.close()
            except Error:
                return Error

class user_delete():
    pass

class Close():
    def close_connection(self,con):
        # # We can also close the connection if we are done with it.
        # # Just be sure any changes have been committed or they will be lost.
        con.close()