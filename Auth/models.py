from sqlite3 import Error
import sqlite3
import os
from Auth.HashPassword import HashPassword
import config

class Singleton(type):
    _instance = None

    def __call__(self, *args, **kwargs):
        if self._instance == None:
            self._instance = super().__call__()
        return self._instance

class Connection(metaclass=Singleton):
    def __init__(self):
        self.con= None
        self.cursor=None
        self._path=None
    
    @property
    def path_address(self):
        return self._path

    @path_address.setter
    def path_address(self,value):
        self._path = value

    def __enter__(self):
        try:
            self.con = sqlite3.connect(self._path, check_same_thread=False)
            self.cursor = self.con.cursor()
            return self.cursor
        except Error:
            return Error

    def __exit__(self, exc_type, exc_val, exc_db):
        try:
            self.cursor.close()
            self.con.commit()
            self.con.close()
            del self.con
        except Error:
            return Error

class CreateTable():
    @staticmethod
    def create_table(myConnection):
        with myConnection as cursor:
            try:
                cursor.execute(f'CREATE TABLE if not exists users ' +
                                f'(id       INTEGER PRIMARY KEY,' +
                                f' email    string(100) UNIQUE,' +
                                f' password string(100) UNIQUE,' +
                                f' active   int,' +
                                f' Lock     int,' +
                                f' incorrectPass int )')
                return True
            except Error:
                return Error

class AddUser():
    def __init__(self, email, password, active, lock, incorrectPass):
        self.email = email
        self.password = password
        self.active = active
        self.lock = lock
        self.incorrectPass = incorrectPass

    def insert_user(self,myConnection):
        with myConnection as cursor:
            # Insert a row of data
            try:
                cursor.execute(f' INSERT INTO users ' +
                                    f' (email,password,active,lock,incorrectPass) ' +
                                    f' VALUES (?,?,?,?,?) ', (self.email, self.password, self.active, self.lock, self.incorrectPass))
                return True
            except:
                return False

class SelectUser:
    def __init__(self,emial):
        self.email=emial
    def select_user(self,myConnection):
        with myConnection as cursor:
            try:
                cursor.execute(f' select id,email,password,active,lock,incorrectPass from users where email=?', (self.email,))
                rows = cursor.fetchall()
                return rows
            except Error:
                return Error 

class UserUpdate():
    def __init__(self,column,id,value):
        self.column=column
        self.id=id
        self.value=value

    def user_update(self,myConnection):
        with myConnection as cursor:
            try:
                cursor.execute(f' update users set {self.column} = ? where id = ? ', (self.value,self.id,))
                return True
            except Error:
                return Error

class UserDelete():
    def __init__(self,emial):
        self.email=emial
    def select_user(self,myConnection):
        with myConnection as cursor:
            try:
                cursor.execute(f' delete from users where email=?', (self.email,))
                return True
            except Error:
                return Error 

class Authentication():
    hp = HashPassword()

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def check_user_password(self,myConnection):
                su= SelectUser(self.email)             
                rows = su.select_user(myConnection)
                if len(rows) > 0:
                    id              =       rows[0][0]
                    password        =       rows[0][2]
                    isactive        =   int(rows[0][3])
                    islock          =   int(rows[0][4])
                    incorrectPass   =   int(rows[0][5])

                    # class hash function for compare password with password in databse 
                    if Authentication.hp.verify_password(password, self.password):

                        if isactive == 0:
                            return 'Account is not active'
                        elif isactive == 1 and islock == 1:
                            return 'Account is Locked'
                        elif isactive == 1 and islock == 0:
                            if incorrectPass>0:
                                # set incorrect value to zero
                                uuip = UserUpdate('incorrectPass',id, 0)
                                uuip.user_update(myConnection)
                            return True
                    else:
                        if islock==1:
                            return 'Account is Locked'
                        else:
                            incorrectPass+=1
                            # read threshold value from config 
                            loginـthreshold = config.Errorـthreshold['time']  
                            if incorrectPass > loginـthreshold:
                                lock_account = UserUpdate('lock',id,1)
                                lock_account.user_update(myConnection)
                                return 'Account locked'
                            else:
                                uuip = UserUpdate('incorrectPass',id, incorrectPass)
                                uuip.user_update(myConnection)
                                return 'Password is not correct!'
                else:
                    return 'Account is not exist'


