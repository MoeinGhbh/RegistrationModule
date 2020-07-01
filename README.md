# Authentication Module

This task has tow part

* Registration
* Authentication

all this functionality implement in models module 
and for unittest use of pytest that run test_models.py

## Registration
A new user can register with their email address and password of choice then call the Models module and insert it to the User table with the hash password.
Once the registration process is complete, the user will receive a confirmation email. This email will contain a link that needs to be clicked on in order to activate the account. 
this linked consists of the ID of a client that calls the activate method, then the status will change.

## Authentication
Users enter their email address and password to log in and faced to different status:
    1- Not register
    2- Not active
    3- Active
    4- Lock
The account will be locked automatically for a certain period of time which defined in the config file, after repeated attempts at logging in with an incorrect password.

### run Module

* python3 run.py

### install and RUN Test

* pip install pytest
* py.test test_models.py -vv

