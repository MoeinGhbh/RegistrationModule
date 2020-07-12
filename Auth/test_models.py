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
    aptusr = AddUser(db,'test@test.com','testpassword',0,0,0)
    res = aptusr.insert_user()
    assert res == True

    a= Authentication(db,'test@test.com','testpassword')
    res = a.authentication()
    assert res == 'Account is not active'

    upur = UserUpdate(db,'active',1,1)
    res = upur.user_update()
    assert res == True

    a= Authentication(db,'test@test.com','testpassword')
    res = a.authentication()
    assert res == 'Account is active'

    a= Authentication(db,'test@test.com','wrongpassword')
    res = a.authentication()
    assert res == 'Password is not correct!'
    a= Authentication(db,'test@test.com','wrongpassword')
    res = a.authentication()
    assert res == 'Password is not correct!'
    a= Authentication(db,'test@test.com','wrongpassword')
    res = a.authentication()
    assert res == 'Password is not correct!'

    a= Authentication(db,'test@test.com','wrongpassword')
    res = a.authentication()
    assert res == 'Account locked'

    a= Authentication(db,'test@test.com','wrongpassword')
    res = a.authentication()
    assert res == 'Account is Locked'




