# Import flask and template operators
from flask import Flask, render_template, current_app, request
from flask_analytics import Analytics
from flask_oauthlib.client import OAuth
import os

# Import the database object from the main app module
from app.database import db_session, init_db

# Import module forms
from app.search.forms import SearchForm, SpotifyForm

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
from app.accounts.controllers import accounts as accounts_module
# Register blueprint(s)
app.register_blueprint(search_module, url_prefix='')
app.register_blueprint(accounts_module, url_prefix='')

oauth = OAuth()
spotify = oauth.remote_app(
    'spotify',
    base_url='https://api.spotify.com',
    request_token_url='https://accounts.spotify.com/api/token',
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize',
  	consumer_key=os.environ['SPOTIFY_CONSUMER_KEY'],
  	consumer_secret=os.environ['SPOTIFY_CONSUMER_SECRET'],
  	# request_token_params={'scope': '-'}
)

oauth.init_app(app)

#Create db
init_db()

from search.mbz_query import MusicBrainzQueryInterface
mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

@app.route('/', methods=['GET','POST'])
def perform_query():
    form_mbz = SearchForm(request.form, prefix="form_mbz")
    form_sptfy = SpotifyForm(prefix="form_sptfy")
    artist, rec, = None, None,
    if form_mbz.validate_on_submit():
        artist = form_mbz['artist_query'].data
        rec = form_mbz['recording_query'].data
        ip_address = request.remote_addr
        commit_to_database(artist,rec,ip_address)
        session['search_results'] = mbz_q.mbz_query(artist=artist, recording=rec)

    if form_sptfy.validate_on_submit():
        spotify_uri = form_sptfy['spotify_uri']

    return render_template('search/search_page.html', form_mbz=form_mbz, form_sptfy=form_sptfy)

def commit_to_database(artist,rec,ip_address):
        artist_bool = True if artist else False
        rec_bool = True if rec else False
        # Commit to Database
        s = Searches(artist_search=artist_bool,recording_search=rec_bool,ip_address=ip_address)
        db_session.add(s)
        if artist:
            artist_s = ArtistSearches(search_id=s.id,search_term=artist)
            db_session.add(artist_s)
        if rec:
            rec_s = RecordingSearches(search_id=s.id,search_term=rec)
            db_session.add(rec_s)
        db_session.commit()
        db_session.close()
