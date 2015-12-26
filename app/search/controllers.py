# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for 
import os, urllib

# Import the database object from the main app module
from app.database import db_session, init_db

# Import module forms
from app.search.forms import SearchForm, SpotifyForm

# Import module models
from app.search.models import Searches, ArtistSearches, RecordingSearches

#Create db
# init_db()

#Import Musicbrainz logic


search = Blueprint('search', __name__, url_prefix='/search')

from app.__init__ import spotify, mbz_q



# Set the route and accepted methods
@search.teardown_app_request
def shutdown_session(exception=None):
    db_session.close()

@spotify.tokengetter
def get_spotify_token(token=None):
    return session.get('spotify_token')

# @search.route('/login')
# def login():
#     return spotify.authorize(callback=url_for('search.oauth_authorized',
#         next=request.args.get('next') or request.referrer or None))

@search.route('/oauth-authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('search.perform_query')
    resp = spotify.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['spotify_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
        )
    session['spotify_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)

        
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



