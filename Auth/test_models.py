import pytest
import sqlite3
from Auth.models import AddUser,UserUpdate,Authentication,CreateTable

@pytest.fixture()
def db():
    conn = sqlite3.connect(':memory:')
    ct = CreateTable()
    ct.create_table(conn)
    return conn

def test_sqlite(db):
    aptusr = AddUser('test@test.com','testpassword',0,0,0)
    res = aptusr.insert_user(db)
    assert res == True

    a= Authentication('test@test.com','testpassword')
    res = a.check_user_password(db)
    assert res == 'Account is not active'

    upur = UserUpdate('active',1,1)
    res = upur.user_update(db)
    assert res == True

    a= Authentication('test@test.com','testpassword')
    res = a.check_user_password(db)
    assert res == True

    a= Authentication('test@test.com','wrongpassword')
    res = a.check_user_password(db)
    assert res == 'Password is not correct!'
    a= Authentication('test@test.com','wrongpassword')
    res = a.check_user_password(db)
    assert res == 'Password is not correct!'
    a= Authentication('test@test.com','wrongpassword')
    res = a.check_user_password(db)
    assert res == 'Password is not correct!'

    a= Authentication('test@test.com','wrongpassword')
    res = a.check_user_password(db)
    assert res == 'Account locked'

    a= Authentication('test@test.com','wrongpassword')
    res = a.check_user_password(db)
    assert res == 'Account is Locked'



