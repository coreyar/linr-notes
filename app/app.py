# Import flask and template operators
from flask import Flask, render_template, current_app
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import os


# Define the WSGI application object
app = Flask(__name__, instance_relative_config=True)
CORS(app)
api = Api(app)

# Configurations
app.config.from_object('config')


# Blueprint(s)
from search.controllers import Search

# Register blueprint(s)
api.add_resource(Search,'/','/search')
