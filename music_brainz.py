import musicbrainzngs as mbz
import os


def authorize(app_name, app_version, contact):
    mbz.auth(os.environ['MUSIC_BRAINZ_API_USERNAME'], os.environ['MUSIC_BRAINZ_API_PASSWORD'])
    mbz.set_useragent(app_name, app_version, contact)


def search_artist(**artist_args):
    search_fields = ["artists", "releases", "recordings"]
    if len(artist_args) > 1:
       return "You may search by %s, %s, or %s" % artist_args
    for arg in artist_args.keys():
        if arg not in search_fields:
            return "Argument not allowed, possible search terms are: %s" % str(search_fields).replace('[', '').replace(']', '')
        else:
            result = getattr(mbz, "search_%s" % arg)(query=artist_args[arg])
            return result