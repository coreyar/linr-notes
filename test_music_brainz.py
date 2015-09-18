import unittest
from music_brainz import *

class TestMusicBrains(unittest.TestCase):

	def test_search_artist_accepts_specific_args(self):
		artist_search = search_artist(**{"smith": 1})
		self.assertEqual(artist_search, "Argument not allowed, required search terms are: 'gender', 'artist', 'type'")


if __name__ in ('main', '__main__'):
	unittest.main()