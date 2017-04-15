import spotipy
from mbz_query import MusicBrainzQueryInterface
from flask_restful import abort

# bad = 'spotify:track:2NfDgUOm9jkGwNtgHBz3dl'
# good = spotify:track:1hu2s7qkm5bo03eODpRQO3

spotify_client = spotipy.Spotify()
mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

def spotify_track(uri):
    results = spotify_client.track(uri)
    album = results['album']['name']
    isrc = results['external_ids']['isrc']
    linr = mbz_q.get_recording_by_isrc(isrc, album)
    for recording in linr:
        for release in recording['recording-list'][0]['release-list']:
            rid = [release['id']]
            title = release['title']
            if results['album']['name'] == title:
                return mbz_q.release_info(rid)
            else:
                abort(500, message='CANNOT FIND {} in MusicBrainz'.format(album))