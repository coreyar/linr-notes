import os
# Import flask and template operators
from flask import Flask, render_template, current_app, request, g, session
from flask_analytics import Analytics
from werkzeug import security

# Import the database object from the main app module
from app.database import db_session, init_db

# Define the WSGI application object
app = Flask(__name__, instance_relative_config=True)
Analytics(app)

# Configurations
app.config.from_object('config')
app.config.from_pyfile('config.py')

#Google Analytics
app.config['ANALYTICS']['GOOGLE_ANALYTICS']['account'] = os.environ['LINR_NOTES_GA']

#Create db
init_db()

from search.mbz_query import MusicBrainzQueryInterface
mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

# Blueprint(s)
from app.search.controllers import search as search_module
# Register blueprint(s)
app.register_blueprint(search_module, url_prefix='')


# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


