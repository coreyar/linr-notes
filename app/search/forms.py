from flask.ext.wtf import Form 

from wtforms import StringField 

class SearchForm(Form):
    artist_query = StringField('Artist')
    recording_query = StringField('Recording')

class SpotifyForm(Form):
	spotify_uri = StringField('Spotify URI')

