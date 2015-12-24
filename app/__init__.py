# Import flask and template operators
from flask import Flask, render_template, current_app
from flask_analytics import Analytics
import os


# Define the WSGI application object
app = Flask(__name__, instance_relative_config=True)
Analytics(app)

# Configurations
app.config.from_object('config')
app.config.from_pyfile('config.py')

#Google Analytics
app.config['ANALYTICS']['GOOGLE_ANALYTICS']['account'] = os.environ['LINR_NOTES_GA']


# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Blueprint(s)
from app.search.controllers import search as search_module

# Register blueprint(s)
app.register_blueprint(search_module, url_prefix='')
