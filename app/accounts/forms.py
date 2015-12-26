from flask.ext.wtf import Form 
from wtforms import StringField, PasswordField

class LoginForm(Form):
	username = StringField('username')
	password = PasswordField('password')