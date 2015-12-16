from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship



# Define a Search model
class Searches(Base):

    __tablename__ = 'search_data'

    id = Column(Integer, primary_key=True)

    # Is artist search
    artist_search = Column(Boolean,  nullable=False)

    # Is recording search
    recording_search = Column(Boolean,  nullable=False)
    
    # Search location
    ip_address = Column(String(192),  nullable=False)

    artist_searches = relationship('ArtistSearches',backref='search_data')

    recording_searches = relationship('RecordingSearches', backref='search_data')

    # New instance instantiation procedure
    def __init__(self, artist_search, recording_search, ip_address):

        self.artist_search = artist_search
        self.recording_search = recording_search
        self.ip_address = ip_address


# Define a Artist Search model
class ArtistSearches(Base):

    __tablename__ = 'artist_search_queries'

    id = Column(Integer, primary_key=True)

    # Foreign Key from Searches 
    search_id = Column(Integer,  ForeignKey('search_data.id'))

    # Query
    search_term = Column(String(200),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, search_id, search_term):

        self.search_id = search_id
        self.search_term = search_term

    def __repr__(self):
        return '<Artist Query: %r>' % (self.search_term)   

# Define a Recording Search model
class RecordingSearches(Base):

    __tablename__ = 'recording_search_queries'

    id = Column(Integer, primary_key=True)

    # Is artist search
    search_id = Column(Integer,  ForeignKey('search_data.id'))

    # Is recording search
    search_term = Column(String(200),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, search_id, search_term):

        self.search_id = search_id
        self.search_term = search_term


    def __repr__(self):
        return '<Recording Query: %r>' % (self.search_term)     

