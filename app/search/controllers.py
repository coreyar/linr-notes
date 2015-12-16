# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for 
import os, urllib
# Import password / encryption helper tools
# from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app.database import db_session, init_db

# Import module forms
from app.search.forms import SearchForm

# Import module models
from app.search.models import Searches, ArtistSearches, RecordingSearches

#Create db
init_db()

#Import Musicbrainz logic
from mbz_query import MusicBrainzQueryInterface
mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

# Define the blueprint: 'auth', set its url prefix: app.url/auth
search = Blueprint('search', __name__, url_prefix='/search')

# Set the route and accepted methods

@search.teardown_app_request
def shutdown_session(exception=None):
    db_session.close()

@search.route('/', methods=['GET','POST'])
def perform_query():
    form = SearchForm(request.form)
    artist, rec, search_results = None, None, None
    if form.validate_on_submit():
        artist = request.form['artist_query']
        rec = request.form['recording_query']
        location = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true' % (request.remote_addr,)).read()
        artist_bool = True if artist else False
        rec_bool = True if rec else False
        # Commit to Database
        s = Searches(artist_search=artist_bool,recording_search=rec_bool,ip_address=location)
        db_session.add(s)
        db_session.commit()
        if artist:
            artist_s = ArtistSearches(search_id=s.id,search_term=artist)
            db_session.add(artist_s)
        if rec:
            rec_s = RecordingSearches(search_id=s.id,search_term=rec)
            db_session.add(rec_s)
        db_session.commit()
        db_session.close()
        ## Commence Search
        search_results = mbz_q.mbz_query(artist=artist, song=rec)
    return render_template('search/search_page.html', search_results=search_results, form=form)
        
@search.route('/<artist_title>/<artist_id>', methods=['GET', 'POST'])
def return_artists(artist_title,artist_id):
    session['releases_list'] = mbz_q.retrieve_albums_by_artist_id(mbz_id=artist_id)
    return render_template('search/album.html')

@search.route('/album/<album_title>/', methods=['GET', 'POST'])
def parse_album_title(album_title):
    album_key = urllib.unquote(urllib.unquote(album_title)) 
    release_display_list = mbz_q.release_info(session['releases_list'][album_key])
    return render_template('search/show_entries.html', release_display_list=release_display_list, album_title=album_key)


