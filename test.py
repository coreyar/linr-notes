import os
import tempfile
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app import app


engine = create_engine('sqlite:///test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class LinrNotesTestCase(unittest.TestCase):

	def setUp(self):
		import app.search.models 
    	Base.metadata.create_all(engine)

	def tearDown(self):
		db_session.close()
		os.remove('test.db')

	def test_index(self):
		tester = app.test_client(self)
		response = tester.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	# def test_artist_search(self):
	# 	tester = app.test_client(self)


if __name__ == '__main__':
	unittest.main()