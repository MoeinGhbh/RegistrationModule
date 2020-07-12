from sqlite3 import Error
import sqlite3
import os
from Auth.HashPassword import HashPassword
import config
import gc

# singleton design pattern for make one instantiate from class
class Singleton(type):
    _instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance

''' connection class make context manager for connecting to database and 
    mangement of open / close and commit
'''
class Connection(metaclass=Singleton):
    def __init__(self):
        self.con = None
        self.cursor = None
        self._path = None

    @property
    def path_address(self):
        return self._path

    @path_address.setter
    def path_address(self, value):
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
            gc.collect()
            self.con = None
            self.cursor = None
        except Error:
            return Error

# create table from Users
class CreateTable:
    @staticmethod
    def create_table(myconnection):
        with myconnection as cursor:
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

# insert user with none active setuation
class AddUser():
    def __init__(self,myConnection, email, password, active, lock, incorrectPass):
        self.myConnection=myConnection
        self.email = email
        self.password = password
        self.active = active
        self.lock = lock
        self.incorrectPass = incorrectPass

    def insert_user(self):
        HP = HashPassword()
        self.password = HP.hash_password(self.password)
        with self.myConnection as cursor:
            # Insert a row of data
            try:
                cursor.execute(f' INSERT INTO users ' +
                               f' (email,password,active,lock,incorrectPass) ' +
                               f' VALUES (?,?,?,?,?) ',
                               (self.email, self.password, self.active, self.lock, self.incorrectPass))

                return True
            except Error:
                return Error

# select class for retreving user from database
class SelectUser:
    def __init__(self,myConnection, emial):
        self.myConnection=myConnection
        self.email = emial

    def select_user(self):
        with self.myConnection as cursor:
            try:
                rows = cursor.execute(f' select id,email,password,active,lock,incorrectPass from users where email=?',
                               (self.email,))
                return list(rows)
            except Error:
                return Error

'''
update 3 diffrenct columns of database
active: for makeing active user
lock:   for lock user after pass threshold which set on config file
incorrectpass: for counting wrong password
'''
class UserUpdate():
    def __init__(self,myConnection, column, id, value):
        self.myConnection=myConnection
        self.column = column
        self.id = id
        self.value = value

    def user_update(self):
        with self.myConnection as cursor:
            try:
                cursor.execute(f' update users set {self.column} = ? where id = ? ', (self.value, self.id,))
                return True
            except Error:
                return Error

# delete user
class UserDelete():
    def __init__(self,myConnection, emial):
        self.myConnection=myConnection
        self.email = emial


    def select_user(self):
        with self.myConnection as cursor:
            try:
                cursor.execute(f' delete from users where email=?', (self.email,))
                return True
            except Error:
                return Error


class Authentication():
    def __init__(self,myConnection, email, password):
        self.myConnection=myConnection
        self.email = email
        self.password = password
        self.rows=None
        self.status=None

        self.id=None
        self.isactive=None
        self.islock=None
        self.incorrectPass=None

    
    def authentication(self):
        self.__check_user()
        if self.rows is not None:
            self.id = self.rows[0][0]
            self.isactive = int(self.rows[0][3])
            self.islock = int(self.rows[0][4])
            self.incorrectPass = int(self.rows[0][5])
            res = self.__check_password()
            if res:
                self.__ckeck_status()
            else:
                self.__password_incorrect()
        return self.status
    

    def __check_user(self):
        su = SelectUser(self.myConnection,self.email)
        rows = su.select_user()
        if len(rows)>0:
            self.rows=rows
        else:
            self.status= 'Account is not exist'

    def __check_password(self):
            password = self.rows[0][2]
            # use this class to hash password            
            hp = HashPassword()
            # class hash function for compare password with password in databse
            if hp.verify_password(password, self.password):
                return True
            else:
                return False
            
    def __set_field_value(self,field,id,value):
         # set incorrect value by value
        uuip = UserUpdate(self.myConnection,field, id, value)
        uuip.user_update()


    def __ckeck_status(self):
        if self.isactive == 0:
            self.status= 'Account is not active'
        elif self.isactive == 1 and self.islock == 1:
            self.status= 'Account is Locked'
        elif self.isactive == 1 and self.islock == 0:
            if self.incorrectPass > 0:
                # set incorrect value to zero
                self.__set_field_value('incorrectPass',self.id,0)
            self.status= 'Account is active'
        
    def __password_incorrect(self):
            if self.islock == 1:
                    self.status= 'Account is Locked'
            else:
                self.incorrectPass += 1
                # read threshold value from config
                loginـthreshold = config.Errorـthreshold['time']
                if self.incorrectPass > loginـthreshold:
                    self.__set_field_value('lock', self.id, 1)
                    self.status= 'Account locked'
                else:
                    self.__set_field_value('incorrectPass',self.id, self.incorrectPass)
                    self.status= 'Password is not correct!'

            

