import spotipy
from mbz_query import MusicBrainzQueryInterface


# uri = 'spotify:track:2NfDgUOm9jkGwNtgHBz3dl'

spotify_client = spotipy.Spotify()
mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')

def spotify_track(uri):
    results = spotify_client.track(uri)
    isrc = results['external_ids']['isrc']
    linr = mbz_q.get_recording_by_isrc(isrc)
    return linr