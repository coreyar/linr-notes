import os
import unittest

from app import app as a
from app.search.models import Searches, ArtistSearches, RecordingSearches
from app.search.controllers import commit_to_database
from app.search.mbz_query import MusicBrainzQueryInterface 

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine('sqlite:///test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

artist = 'The Hold Steady'
recording = 'Your Little Hoodrat Friend'

class LinrNotesTestCase(unittest.TestCase):

    def setUp(self,):
        a.config['TESTING'] = True
        a.config['CSRF_ENABLED'] = False
        from app.search.models import *
        Base.metadata.create_all(engine)
        self.mbz_q = MusicBrainzQueryInterface('Linr Notes', '0.0.1', 'coreyarice@gmail.com')
 

    def tearDown(self):
        db_session.close()
        os.remove('test.db')

    def test_index(self):
        tester = a.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

#Test how app functions with artist only searches that return one artist
    def test_artist_search_form(self,):
        with a.test_client(self) as c:
            response = c.post('/', data=dict(
                artist_query='Greenday',submit=True),follow_redirects=True)
        assert 'value="Greenday"' in response.data

    def test_recording_search_form(self,):
        tester = a.test_client(self)
        response = tester.get('/', data=dict(
            recording_query='Sweet Child of Mine',submit=True),follow_redirects=True)
        assert 'value="Sweet Child of Mine"' in response.data
        
    def test_artist_only(self):
        s = Searches(artist_search=True,recording_search=False,ip_address='local')
        db_session.add(s)
        db_session.commit()
        artist_s = ArtistSearches(search_id=s.id,search_term=artist)
        db_session.add(artist_s)
        db_session.commit()
        self.assertEqual(artist_s, db_session.query(ArtistSearches).filter(ArtistSearches.search_id == s.id).first())

    def test_recording_only(self):
        s = Searches(artist_search=False,recording_search=True,ip_address='local')
        db_session.add(s)
        db_session.commit()
        rec_s = RecordingSearches(search_id=s.id,search_term=recording)
        db_session.add(rec_s)
        db_session.commit()
        self.assertEqual(rec_s, db_session.query(RecordingSearches).filter(RecordingSearches.search_id == s.id).first())
        

    def test_artist_and_recording(self):
        s = Searches(artist_search=True,recording_search=False,ip_address='local')
        db_session.add(s)
        db_session.commit()
        artist_s = ArtistSearches(search_id=s.id,search_term=artist)
        rec_s = RecordingSearches(search_id=s.id,search_term=recording)
        db_session.add_all([rec_s, artist_s])
        db_session.commit()
        expected = [(artist_s, rec_s)]
        self.assertEqual(expected,
            db_session.query(ArtistSearches, RecordingSearches).filter(RecordingSearches.search_id == s.id).filter(ArtistSearches.search_id == s.id).all())

    def test_mbz_query_no_recording(self):
        result = self.mbz_q.mbz_query(artist=artist,recording=None)
        self.assertEqual([None, True],[result['recordings'], result['artists'] != None ])

    def test_mbz_query_no_artist(self):
        result = self.mbz_q.mbz_query(artist=None,recording=recording)
        self.assertEqual([True, None],[result['recordings'] != None, result['artists']])

    def test_retrieve_albums_by_artist_id(self):
        result = self.mbz_q.retrieve_albums_by_artist_id()
        assert type(result) == dict

    def test_release_info(self):
        result = self.mbz_q.release_info()
        self.assertEqual([None, True],[result['recordings'], result['artists'] != None ])







if __name__ == '__main__':
    unittest.main()