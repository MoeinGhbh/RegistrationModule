from Auth.models import Connection,CreateTable,add_user,user_update,user_delete
import pytest


class TestClass:
    email='test@test.com'
    password='1234567890'

    @pytest.fixture
    def sql_connection(self):
        connect =  Connection()
        return connect.sql_connection()

    def test_createTable(self,sql_connection):
        pass

    def test_add_user(self,sql_connection):
        user = add_user(TestClass.email,TestClass.password)
        assert user.insert_value() == True

    def test_user_update(self,sql_connection):
        pass

    def test_user_delete(self,sql_connection):
        pass

