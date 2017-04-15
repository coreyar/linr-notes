import musicbrainzngs as mbz
import os, json, requests, datetime
from operator import itemgetter
from collections import defaultdict

caa = 'http://coverartarchive.org'

class MusicBrainzQueryInterface():

    def __init__(self, app_name, app_version, contact):
        self.auth = mbz.auth(os.environ['MUSIC_BRAINZ_API_USERNAME'], os.environ['MUSIC_BRAINZ_API_PASSWORD'])
        self.set_useragent = mbz.set_useragent(app_name, app_version, contact)

    def mbz_query(self, artist, recording):
        query_dict = {'recordings': None,'artists': None}
        if recording:
            query_dict['recordings'] = mbz.search_recordings(recording, artist)
            return query_dict
        elif artist:
            query_dict['artists'] = mbz.search_artists(artist)
            return query_dict
        else:
            return None

    def retrieve_albums_by_artist_id(self, mbz_id):
        album_response = mbz.get_artist_by_id(mbz_id, includes=['releases'])
        album_dict = defaultdict(list)
        for release in album_response['artist']['release-list']:
            album_dict[release['title']].append(release['id'])
        return dict(album_dict)

    def release_info(self, release_list):
        ##Need to clean up data list to include only necessary data
        data = ['artists', 'labels', 'recordings', 'release-groups', 'media', 'artist-credits', 'discids', 
         'isrcs', 'recording-level-rels', 'work-level-rels', 'annotation', 'aliases', 'area-rels', 'artist-rels', 'label-rels', 'place-rels',  
         'recording-rels', 'release-rels', 'release-group-rels', 'url-rels', 'work-rels']
        # data = ['artists', 'labels', 'recordings', 'media', 'release-groups', 'release-rels', 'artist-rels']
        image = False
        formats = ''
        release_date = ''
        labels = ''
        release_display_list = []
        ########
        #Shortening Release list because long release lists cause timeout
        #######
        release_list = release_list[0:5]

        for release in release_list:
            album_data =  mbz.get_release_by_id(release, includes=data) 
            labels = [label['label']['name'] for label in album_data['release']['label-info-list']]
            try:
                formats = [medium['format'] for medium in album_data['release']['medium-list']]
            except KeyError:
                pass
            tracks = album_data['release']['medium-list'][0]['track-list']
            if album_data['release']['cover-art-archive']['artwork'] == 'true':
                r = requests.get('{0}/release/{1}'.format(caa, release)).json()
                image = r['images'][0]['image']
            try:
                release_date = datetime.datetime.strptime(album_data['release']['release-group']['first-release-date'], '%Y-%m-%d').strftime("%B %d, %Y")
            except ValueError:
                release_date = album_data['release']['release-group']['first-release-date']
            release_display_list.append({'image':image, 'tracks':tracks, 'labels':labels, 
                'formats':formats, 'release_date': release_date })
        return release_display_list

    def recording_parser(self, results):
        list_of_recordings = []
        #If Musicbrainz data is missing
        artist_name = ''
        title = ''
        rec_type = ''
        rec_type_title = ''
        status = ''
        recording_data = ['artists', 'releases', 'discids', 'media', 'artist-credits', 'isrcs', 'annotation', 
                        'aliases', 'tags', 'user-tags', 'ratings', 'user-ratings', 'area-rels', 'artist-rels', 
                        'label-rels', 'place-rels', 'recording-rels', 'release-rels', 
                        'release-group-rels', 'url-rels', 'work-rels']
        # for recording in results['recording-list']:
        rec_result = mbz.get_recording_by_id(results, includes=recording_data)
        # list_of_recordings.append({'title': recording['title'],
        #                             'rec_id':recording['id'], 
        #                             'rel_id':[rel['id'] for rel in rec_result['recording']['release-list']]})
        list_of_recordings = [rel['id'] for rel in rec_result['recording']['release-list']]
        parsed_list_of_recordings = self.release_info(list_of_recordings)
        return parsed_list_of_recordings


    def get_recording_by_isrc(self, isrc):
        results = mbz.get_recordings_by_isrc(isrc)
        id_list = []
        for each in results['isrc']['recording-list']:
            id_list.append(each['id'])
        return mbz.search_recordings(rid=id_list[0])

def parse_artist_list(result):
    list_of_artists = []
    for artist in result['artist-list']:
        list_of_artists.append({'id':artist['id'],'name':artist['name']})
    return list_of_artists


