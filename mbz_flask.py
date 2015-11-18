import os, urllib
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from contextlib import closing
from flask_analytics import Analytics
from flaskext.mysql import MySQL
from mbz_query import MusicBrainzQueryInterface

app = Flask(__name__)
mysql = MySQL()
Analytics(app)


#Configure Musicbrainz API Requests
mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

# Analytics
app.config['ANALYTICS']['GOOGLE_ANALYTICS']['account'] = os.environ['LINR_NOTES_GA']
#Configure MySQL Database
app.config['MYSQL_DATABASE_USER'] = os.environ['LINR_NOTES_DB_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['LINR_NOTES_DB_PW']
app.config['MYSQL_DATABASE_HOST'] = os.environ['LINR_NOTES_DATABASE_HOST']
app.config['MYSQL_DATABASE_DB'] = os.environ['LINR_NOTES_DATABASE_DB']
mysql.init_app(app)


#Ensure Database has been created
with app.app_context():
	conn = mysql.connect()
	cur = conn.cursor()
	with open('linr_notes.sql', 'r') as mysql_file:
		sqlCommands = mysql_file.read().split(';')
		for command in sqlCommands:
			try:
				cur.execute(command)
			except:
				pass

@app.before_request
def before_request():
	with app.app_context():
		conn = mysql.connect()
		cur = conn.cursor()

@app.route('/', methods=['GET','POST'])
def perform_query():
	artist, song, search_results = None, None, None
	if request.method == 'POST':
		artist = request.form['artist']
		song = request.form['song']
		location = urllib.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true' % (request.remote_addr,)).read()
		artist_bool = 1 if artist else 0
		song_bool = 1 if song else 0
		cur.execute("""INSERT INTO searches (artist_search, recording_title_search, ip_address) values ('%d', '%d','%s');
		   """ % (artist_bool, song_bool, location))
		cur.execute('SELECT LAST_INSERT_ID() INTO @last_search_id;')
		if artist:
			cur.execute("INSERT INTO artist_searches (search_id, search_term) values (@last_search_id,'%s');" % (artist,))
		if song:
			cur.execute("INSERT INTO recording_searches (search_id, search_term) values (@last_search_id,'%s');" % (song,))
		conn.commit()
		try:
			search_results = mbz_q.mbz_query(artist=artist, song=song)
		except ValueError:
			return render_template('search_page.html', display_results=search_results)
		try: 
			if search_results['artist']:
				return render_template('artist.html', artist_results=search_results)
			if search_results['song']:
				return render_template('song.html', song_results=search_results)
		except (TypeError, KeyError) as e:
			session['releases_list'] = search_results
			return render_template('album.html')
	return render_template('search_page.html', artist_results=search_results)
		
@app.route('/<artist_title>/<artist_id>', methods=['GET', 'POST'])
def return_artists(artist_title,artist_id):
	session['releases_list'] = mbz_q.retrieve_albums_by_artist_id(mbz_id=artist_id)
	return render_template('search_page.html')

@app.route('/album/<album_title>/', methods=['GET', 'POST'])
def parse_album_title(album_title):	
	release_display_list = mbz_q.release_info(session['releases_list'][album_title])
	return render_template('show_entries.html', release_display_list=release_display_list, album_title=album_title)


if __name__ == '__main__':
	app.secret_key = os.environ['SECRET_KEY']
	app.run()

