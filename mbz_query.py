import musicbrainzngs as mbz
import os
import json
import requests

# import sqlite3
#
# def create_table():
#     with sqlite3.connect("output.db") as db:
#         db.execute("""CREATE TABLE IF NOT EXISTS artists (
#             id INTEGER PRIMARY KEY,
#             artist_name STRING,
#             music_brainz_id STRING
#             )""")
#         db.commit()

caa = 'http://coverartarchive.org'

class MusicBrainzQueryInterface():

    def __init__(self, app_name, app_version, contact):
        self.auth = mbz.auth(os.environ['MUSIC_BRAINZ_API_USERNAME'], os.environ['MUSIC_BRAINZ_API_PASSWORD'])
        self.set_useragent = mbz.set_useragent(app_name, app_version, contact)
        # self.db = sqlite3.connect("output.db")

    def mbz_query(self, artist, song=None):
        results = None
        if artist and not song:
            result = getattr(mbz, "search_artists")(artist)
            if result['artist-count'] == 1:
                mbz_id = result['artist-list'][0]['id']
                artist_rec_dict = getattr(mbz, "get_artist_by_id")(mbz_id, includes=['releases'])
                results = parse_artist_rel_dict(artist_rec_dict)
            else:
                print 'Try again'
        if song:
            results = getattr(mbz,"search_recordings")(song, artist=artist)
        print results
        return results

    def artist_parser(self, result):
        """
        Store Artist Name, ID
        """
        return dict(artist_name=result['artist-list'][0]['name'], 
                    music_brainz_id=result['artist-list'][0]['id'])

    def update_artist_database(self, artist_dict):
        with self.db:
            self.db.execute("INSERT INTO artists (artist_name, artist_music_brainz_id) VALUES ('%s', '%s')" % (artist_dict['artist_name'], artist_dict['music_brainz_id']))
            self.db.commit()

    def release_info(self, song_id):
        data = ['artists', 'labels', 'recordings', 'release-groups', 'media', 'artist-credits', 'discids', 
        'isrcs', 'recording-level-rels', 'work-level-rels', 'annotation', 'aliases', 'area-rels', 'artist-rels', 'label-rels', 'place-rels',  
        'recording-rels', 'release-rels', 'release-group-rels', 'url-rels', 'work-rels']
        song_data =  mbz.get_release_by_id(song_id, includes=data) #'media', 'labels','recordings']
        print song_data['release']['medium-list'][0].keys()
        labels_list = []
        for label in song_data['release']['label-info-list']:
            labels_list.append(label['label']['name'])
        tracks = song_data['release']['medium-list'][0]['track-list']
        # release_date = song_data['release']['date']
        if song_data['release']['cover-art-archive']['artwork'] == 'true':
            r = requests.get('{0}/release/{1}'.format(caa, song_id)).json()
            image = r['images'][0]['image']

        return image, tracks, labels_list

def parse_artist_rel_dict(recording_list):
    dict_of_recordings = {}
    for rec in recording_list['artist']['release-list']:
        dict_of_recordings.update({rec['title']:rec['id']})
    print dict_of_recordings
    return dict_of_recordings

def create_track_time():
    return track_time


