from flask_restful import Resource, reqparse
from spotify_query import spotify_track

import os, urllib



class Search(Resource):
    def get(self, track):
        parser = reqparse.RequestParser()
        parser.add_argument('track', type=str, help='Spotify Song/Track URI')
        args = parser.parse_args()
        return spotify_track(track)

