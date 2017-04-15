from flask_restful import Resource

import os, urllib

class Search(Resource):
    def post(self):
        # Default to 200 OK
        return {'task': 'Hello world'}



