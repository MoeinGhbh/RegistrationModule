from sqlite3 import Error
import sqlite3
import os
from Auth.HashPassword import HashPassword


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

                    if Authentication.hp.verify_password(password, self.password):
                        print('password is correct')
                        print(rows)
                        if len(rows) > 0:
                            if isactive == 0:
                                return 'Account is not active'
                            elif isactive == 1 and islock == 0:
                                return True
                            elif isactive == 1 and islock == 1:
                                return 'Account is Locked'
                        else:
                            return 'Account is not exist'
                    else:
                        uuip = UserIncorrectPass(id, incorrectPass)
                        uuip.user_update()
                        return 'password is not correct!'

            except Error:
                return Error

from abc import ABC,abstractclassmethod

class UserUpdate:
    @abstractclassmethod
    def user_update(self):
        pass

class UpserActive(UserUpdate):
    def __init__(self,id):
        self.id=id
        
    def user_update(self):
        with Connection() as cursor:
            # select a row from data
            try:
                cursor.execute(
                    f' update users set active = 1 where id = ? ', (self.id,))
                return True
            except Error:
                return Error

class UserLock(UserUpdate):
    def __init__(self,id,lock):
        self.id=id
        self.lock=lock

    def user_update(self):
        with Connection() as cursor:
            # select a row from data
            try:
                cursor.execute(f' update users set lock = ? where id = ? ',(self.lock,self.id))
            except Error:
                return Error
        
class UserIncorrectPass(UserUpdate):
    def __init__(self,id,incorrectPass):
        self.id=id
        self.incorrectPass=incorrectPass

    def user_update(self):
        with Connection() as cursor:
            # select a row from data
            self.incorrectPass+=1
            # hhhhhhhhhhhaaaaaaaaaaaaaaaaaaaaaaarrrrrrrrrrrrrdddddddd code
            if self.incorrectPass > 3:
                lock_account = UserLock(self.id,1)
                lock_account.user_update()
            else:
                try:
                    cursor.execute(f'  UPDATE users set incorrectPass = ? where id = ? ',(self.incorrectPass,self.id))
                except Error:
                    return Error

class UserDelete():
    pass

class Close():
    def close_connection(self,con):
        # # We can also close the connection if we are done with it.
        # # Just be sure any changes have been committed or they will be lost.
        con.close()
