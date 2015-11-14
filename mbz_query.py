import musicbrainzngs as mbz
import os, json, requests
from operator import itemgetter
from collections import defaultdict
from flask import session

caa = 'http://coverartarchive.org'

class MusicBrainzQueryInterface():

    def __init__(self, app_name, app_version, contact):
        self.auth = mbz.auth(os.environ['MUSIC_BRAINZ_API_USERNAME'], os.environ['MUSIC_BRAINZ_API_PASSWORD'])
        self.set_useragent = mbz.set_useragent(app_name, app_version, contact)
        # self.db = sqlite3.connect("output.db")

    def mbz_query(self, artist, song):
        if song:
            return recording_parser(mbz.search_recordings(song, artist))
        else:
            results = mbz.search_artists(artist) 
            if results['artist-count'] == 1:
                mbz_id = results['artist-list'][0]['id']
                return self.retrieve_albums_by_artist_id(mbz_id)
            else:
                return {'artist':parse_artist_list(results)}

    def retrieve_albums_by_artist_id(self, mbz_id):
        album_response = mbz.get_artist_by_id(mbz_id, includes=['releases'])
        album_dict = defaultdict(list)
        for release in album_response['artist']['release-list']:
            album_dict[release['title']].append(release['id'])
        return dict(album_dict)


    def artist_parser(self, result):
        return dict(artist_name=result['artist-list'][0]['name'], 
                    music_brainz_id=result['artist-list'][0]['id'])

    def release_info(self, release_list):
        data = ['artists', 'labels', 'recordings', 'release-groups', 'media', 'artist-credits', 
        'recording-level-rels', 'work-level-rels', 'artist-rels', 'label-rels', 'place-rels',  
        'recording-rels', 'release-rels', 'release-group-rels', 'work-rels']
        release_display_list = []
        for release in release_list:
            image = False
            album_data =  mbz.get_release_by_id(release, includes=data) 
            labels = [label['label']['name'] for label in album_data['release']['label-info-list']]
            tracks = album_data['release']['medium-list'][0]['track-list']
        # release_date = song_data['release']['date']
            if album_data['release']['cover-art-archive']['artwork'] == 'true':
                r = requests.get('{0}/release/{1}'.format(caa, release)).json()
                image = r['images'][0]['image']
            release_display_list.append({'image':image, 'tracks':tracks, 'labels':labels, 'title':'' })
        return release_display_list

##Series of functions to parse Musicbrainz results

# def create_track_time():
#     return track_time

def recording_parser(results):
    list_of_recordings = []
    artist_name = ''
    title = ''
    rec_type = ''
    rec_type_title = ''
    status = ''
    for recording in results['recording-list']:
        try:
            artist_name = recording['artist-credit'][0]['artist']['name'] 
        except KeyError:
            pass
        try:
            title = recording['title']
        except KeyError:
            pass
        try:
            rec_type = recording['release-list'][0]['release-group']['primary-type'] 
        except KeyError:
            pass
        try:
            for release in recording['release-list']:
                rec_type_title = release['title'] 
        except KeyError:
            pass
        try:
            for rel_stat in recording['release-list']:
                status = rel_stat['status'] 
        except KeyError:
            pass
        try:
            for rel_alb_id in recording['release-list']:
                alb_id = rel_alb_id['id']
        except KeyError:
            pass
        display_title = artist_name + ' - ' + title + ' (' + rec_type + ': ' + rec_type_title + ', ' + status + ')'
        rec_id = recording['id']
        list_of_recordings.append({'id':alb_id,'name':display_title})
    return list_of_recordings

def parse_artist_list(result):
    list_of_artists = []
    print result['artist-list']
    for artist in result['artist-list']:
        list_of_artists.append({'id':artist['id'],'name':artist['name']})
    return list_of_artists


