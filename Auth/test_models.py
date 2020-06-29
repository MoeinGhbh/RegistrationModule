from Auth.models import Connection,CreateTable,AddUser
import pytest


class TestClass:
    email='testaaaaa@test.com'
    password='aaaa1234567890'


    @pytest.fixture
    def sql_connection(self):
        connect =  Connection()
        connect._path=":memory:"

    def test_createTable(self,sql_connection):
        crttbl =  CreateTable()
        assert crttbl.create_table() == True

    def test_add_user(self,sql_connection):
        newUser = AddUser(TestClass.email, TestClass.password,0,0,0)
        assert newUser.insert_user() == True
   
    # def test_user_update(self,sql_connection):
    #     pass

    # def test_user_delete(self,sql_connection):
    #     pass

