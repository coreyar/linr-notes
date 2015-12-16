#Production Settingse

DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

#TODO - Define Production Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')


# Application threads. 
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

#Secret key for signing the data. 
CSRF_SESSION_KEY = os.environ['SECRET_KEY']

# Secret key for signing cookies
SECRET_KEY = os.environ['SECRET_KEY']


