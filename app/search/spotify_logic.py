import spotipy
import os

spotify = spotipy.Spotify()


def mbz_search_dict(sp_uri):
	spotify.track(sp_uri)
