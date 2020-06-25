
# Registration Module

Many websites allow their visitors to create a customized personal account. This is
usually done through a web interface that allows new users to register by completing a
registration form.
This task includes designing and implementing a backend that possesses the functions
outlined below. The necessary data should be stored in an SQL database. Please
develop a suitable schema and create a Python module that provides the functionality
described below. For this task, it is not expected of you to connect a website (or even
to write HTML for the site), to maintain web sessions via cookies or the like.

## Registration

A new user can register with their email address and password of choice. Once the
registration process is complete, the user will receive a confirmation email. This email
will contain a link that needs to be clicked on in order to activate the account. Note:
Sending an actual email or routing the request when the user clicks on the activation
link is not part of the task.

## Authentication

Users enter their email address and password to log in. The account will be locked
automatically for a certain period of time after repeated attempts at logging in with an
incorrect password.