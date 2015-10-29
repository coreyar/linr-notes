import os
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from contextlib import closing
from flask.ext.bootstrap import Bootstrap
from flaskext.mysql import MySQL
from mbz_query import MusicBrainzQueryInterface
from flask_analytics import Analytics
import urllib


app = Flask(__name__)
mysql = MySQL()
Analytics(app)
bootstrap = Bootstrap(app)


#Configure Musicbrainz API Requests
mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

# Analytics
app.config['GOOGLE_ANALYTICS']['ACCOUNT'][os.environ['LINR_NOTES_GA']
#Configure MySQL Database
app.config['MYSQL_DATABASE_USER'] = os.environ['LINER_NOTES_DB_PW']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['LINR_NOTES_MYSQL_DATABASE_USER']
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'linr_notes'
mysql.init_app(app)


with app.app_context():
	conn = mysql.connect()
	cur = conn.cursor()
	cur.execute("""CREATE DATABASE IF NOT EXISTS linr_notes;""") 
	cur.execute("""CREATE TABLE IF NOT EXISTS linr_notes.searches(
	            id INTEGER PRIMARY KEY AUTO_INCREMENT,
	            artist_name TEXT,
	            musicbrainz_artist_id TEXT,
	            recording_title TEXT,
	            musicbrainz_recording_id TEXT,
	            location TEXT);""")

@app.before_request
def before_request():
	with app.app_context():
		conn = mysql.connect()
		cur = conn.cursor()

@app.route('/', methods=['GET','POST'])
def perform_query():
	artist = None
	song = None
	search_results = None
	rec_titles = None 
	if request.method == 'POST':
		artist = request.form['artist']
		song = request.form['song']
		ip = request.remote_addr
		response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true' % (ip,)).read()
		print response
		cur.execute('Use linr_notes;')
		# row_id = cur.rownumber
		# row_id += 1
		cur.execute("INSERT INTO searches (id,artist_name) values ('%s');" % (artist,))
		conn.commit()
		search_results = mbz_q.mbz_query(artist=artist, song=song)
		try: 
			if search_results['artist']:
				return render_template('show_entries.html', artist_results=search_results)
		except KeyError:
			# cur.execute('INSERT INTO linr_notes.searches (artist_name, recording_title) values (?,?)', [artist, song])
			return render_template('show_entries.html', display_results=search_results)
	# cur.execute('INSERT INTO linr_notes.searches (artist_name, recording_title) values (?,?)', [artist, song])
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
	app.run(debug=True)

