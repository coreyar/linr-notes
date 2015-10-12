import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from contextlib import closing
from flask.ext.bootstrap import Bootstrap
from mbz_query import MusicBrainzQueryInterface


###configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'



# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
bootstrap = Bootstrap(app)

mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET','POST'])
def perform_query():
	artist = None
	song = None
	search_results = None
	rec_titles = None 
	if request.method == 'POST':
		artist = request.form['artist']
		song = request.form['song']
		search_results = mbz_q.mbz_query(artist=artist, song=song)
		try: 
			if search_results['artist']:
				print search_results
				print 'yes'
				return render_template('show_entries.html', artist_results=search_results)
		except KeyError:
	# if artist and not song:
	# 	return render_template('show_entries.html', display_results=search_results)
	# else: 
	# 	pass
			return render_template('show_entries.html', display_results=search_results)
	return render_template('show_entries.html', display_results=search_results)

@app.route('/artists/<artist_title>/<artist_id>', methods=['GET', 'POST'])
def return_artists(artist_title,artist_id):
	search_results = mbz_q.retrieve_albums_by_artist_id(artist_id)
	return render_template('show_entries.html', display_results=search_results)

@app.route('/recording/<song_title>/<song_id>', methods=['GET', 'POST'])
def parse_song_title(song_title, song_id):
	image, tracks, labels_list = mbz_q.release_info(song_id)
	return render_template('recording.html', image=image, tracks=tracks)

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] !=app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))


if __name__ == '__main__':
	app.run()

