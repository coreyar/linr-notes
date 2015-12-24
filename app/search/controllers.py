# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for 
import os, urllib

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


search = Blueprint('search', __name__, url_prefix='/search')

# Set the route and accepted methods

@search.teardown_app_request
def shutdown_session(exception=None):
    db_session.close()

@search.route('/', methods=['GET','POST'])
def perform_query():
    form = SearchForm(request.form)
    artist, rec, search_results, = None, None, None
    if form.validate_on_submit():
        artist = request.form['artist_query']
        rec = request.form['recording_query']
        ip_address = request.remote_addr
        commit_to_database(artist,rec,ip_address)
    session['search_results'] = mbz_q.mbz_query(artist=artist, recording=rec)
    return render_template('search/search_page.html', form=form)

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

        
@search.route('/<artist_title>/<artist_id>', methods=['GET', 'POST'])
def return_artists(artist_title,artist_id):
    session['releases_list'] = mbz_q.retrieve_albums_by_artist_id(mbz_id=artist_id)
    return render_template('search/album.html')

@search.route('/album/<album_title>/', methods=['GET', 'POST'])
def parse_album_title(album_title):
    album_key = urllib.unquote(urllib.unquote(album_title))
    album_release_list = session['releases_list'][album_key]
    release_display_list = mbz_q.release_info(album_release_list)
    return render_template('search/show_entries.html', release_display_list=release_display_list, album_title=album_key)

@search.route('/recording/<recording_title>/<rec_id>', methods=['GET', 'POST'])
def recording_release_page(recording_title, rec_id):
    recording_title = urllib.unquote(urllib.unquote(recording_title))
    result = mbz_q.recording_parser(rec_id)
    return render_template('search/show_entries.html',release_display_list=result)



