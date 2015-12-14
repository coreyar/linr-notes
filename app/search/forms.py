# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField # PasswordField BooleanField

# Import Form validators
# from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class SearchForm(Form):
    artist_query = TextField('Email Address')
    recording_query = TextField('Password')



