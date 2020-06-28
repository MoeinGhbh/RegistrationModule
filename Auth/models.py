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
    DEFAULT_PATH = os.path.join(
        os.path.dirname(__file__), '../albeton.sqlite3')

    # create a default path to connect to and create (if necessary) a database
    # called 'database.sqlite3' in the same directory as this script
    def __init__(self):
        self.con= None
        self.cursor=None

    def __enter__(self, db_path=DEFAULT_PATH):
        try:
            self.con = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.con.cursor()
            return self.cursor
        except Error:
            return Error

    def __exit__(self, exc_type, exc_val, exc_db):
        try:
            self.cursor.close()
            self.con.commit()
            self.con.close()
        except Error:
            return Error
        


class CreateTable():
    @staticmethod
    def create_table():
        with Connection() as cursor:
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

    def insert_user(self):
        with Connection() as cursor:
            # Insert a row of data
            try:
                cursor.execute(f' INSERT INTO users ' +
                                    f' (email,password,active,lock,incorrectPass) ' +
                                    f' VALUES (?,?,?,?,?) ', (self.email, self.password, self.active, self.lock, self.incorrectPass))
                # Save (commit) the changes
                return True
            except:
                return False


class Authentication():
    hp = HashPassword()

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def check_user_password(self):
        with Connection() as cursor:
            # select a row from data
            try:
                cursor.execute(
                    f' select id,email,password,active,lock,incorrectPass from users where email=?', (self.email,))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    id = rows[0][0]
                    password = rows[0][2]
                    isactive = int(rows[0][3])
                    islock = int(rows[0][4])
                    incorrectPass = int(rows[0][5])

                    # class hash function for compare password with password in databse 
                    if Authentication.hp.verify_password(password, self.password):

                        if isactive == 0:
                            return 'Account is not active'
                        elif isactive == 1 and islock == 1:
                            return 'Account is Locked'
                        elif isactive == 1 and islock == 0:
                            if incorrectPass>0:
                                # set incorrect value to zero
                                uuip = UserIncorrectPass()
                                uuip.user_update(id, 0)
                            return True
                    else:
                        if islock==1:
                            return 'Account is Locked'
                        else:
                            incorrectPass+=1
                            # read threshold value from config 
                            loginـthreshold = config.Errorـthreshold['time']  
                            if incorrectPass > loginـthreshold:
                                lock_account = UserLock()
                                lock_account.user_update(id,1)
                                return 'Account locked'
                            else:
                                uuip = UserIncorrectPass()
                                uuip.user_update(id, incorrectPass)
                                return 'Password is not correct!'
                else:
                    return 'Account is not exist'
            except Error:
                return Error

from abc import ABC,abstractclassmethod

class UserUpdate:
    @abstractclassmethod
    def user_update(self):
        pass

class UpserActive(UserUpdate):
    def user_update(self,id,active):
        with Connection() as cursor:
            try:
                cursor.execute(f' update users set active = ? where id = ? ', (active,id,))
                return True
            except Error:
                return Error

class UserLock(UserUpdate):
    def user_update(self,id,lock):
        with Connection() as cursor:
            try:
                cursor.execute(f' update users set lock = ? where id = ? ',(lock,id))
            except Error:
                return Error
        
class UserIncorrectPass(UserUpdate):
    def user_update(self,id,incorrectPass):
        with Connection() as cursor:
            try:
                cursor.execute(f'  UPDATE users set incorrectPass = ? where id = ? ',(incorrectPass,id))
            except Error:
                return Error

class UserDelete():
    pass

