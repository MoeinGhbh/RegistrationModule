from Auth.models import CreateTable,AddUser,Connection
import pytest
import sqlite3
from sqlite3 import Error
from Auth.models import Connection

class TestClass:
    email='aaatestaasdfaaaa@test.com'
    password='gggggf234567890'

    @pytest.fixture(scope='function')
    def sql_connection(self):
        MyConnection= Connection()
        MyConnection._path=':memory:'
        return MyConnection
        # CreateTable().create_table(MyConnection)

    def test_createTable(self,sql_connection):
        print(sql_connection)
        # print(sql_connection._p)
        crttbl =  CreateTable()
        assert crttbl.create_table(sql_connection) == True

    def test_add_user(self,sql_connection):
        newUser = AddUser(TestClass.email, TestClass.password,0,0,0)
        assert newUser.insert_user(sql_connection) == True
   
    # def test_user_update(self,sql_connection):
    #     pass

    # def test_user_delete(self,sql_connection):
    #     pass

