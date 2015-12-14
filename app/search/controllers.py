# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
import os, urllib
# Import password / encryption helper tools
# from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.search.forms import SearchForm

# Import module models (i.e. User)
from app.search.models import Searches

#Import Musicbrainz logic
from mbz_query import MusicBrainzQueryInterface
mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

# Define the blueprint: 'auth', set its url prefix: app.url/auth
search = Blueprint('search', __name__, url_prefix='/search')

# Set the route and accepted methods

@search.route('/', methods=['GET','POST'])
def perform_query():
    form = SearchForm(request.form)
    artist, song, search_results = None, None, None
    if form.validate_on_submit():
        artist = request.form['artist_query']
        song = request.form['recording_query']
        location = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true' % (request.remote_addr,)).read()
        artist_bool = 1 if artist else 0
        song_bool = 1 if song else 0
        ## Commit to Database
        cur.execute("""INSERT INTO searches (artist_search, recording_title_search, ip_address) values ('%d', '%d','%s');
           """ % (artist_bool, song_bool, location))
        cur.execute('SELECT LAST_INSERT_ID() INTO @last_search_id;')
        if artist:
            cur.execute("INSERT INTO artist_searches (search_id, search_term) values (@last_search_id,'%s');" % (artist,))
        if song:
            cur.execute("INSERT INTO recording_searches (search_id, search_term) values (@last_search_id,'%s');" % (song,))
        conn.commit()
        ## Commence Search
        search_results = mbz_q.mbz_query(artist=artist, song=song)

        # except ValueError:
        #   return render_template('search_page.html', display_results=search_results)
        # try: 
        #   if search_results['artist']:
        #       return render_template('artist.html', artist_results=search_results)
        #   elif search_results['song']:
        #       return render_template('song.html', song_results=search_results)
        # except (KeyError,TypeError) as e:
        #   session['releases_list'] = search_results
        #   return render_template('album.html')
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


