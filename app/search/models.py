# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a Search model
class Searches(Base):

    __tablename__ = 'search_data'

    # Is artist search
    artist_search = db.Column(db.Boolean,  nullable=False)

    # Is recording search
    recording_search = db.Column(db.Boolean,  nullable=False)
    
    # Search location
    ip_address = db.Column(db.String(192),  nullable=False)

    artist_searches = db.relationship('ArtistSearches',backref='search_data')

    recording_searches = db.relationship('RecordingSearches', backref='search_data')

    # New instance instantiation procedure
    def __init__(self, artist_search, recording_search, ip_address):

        self.artist_search = artist_search
        self.recording_search = recording_search
        self.ip_address = ip_address


# Define a Artist Search model
class ArtistSearches(Base):

    __tablename__ = 'artist_search_queries'

    # Foreign Key from Searches 
    search_id = db.Column(db.Integer,  db.ForeignKey('search_data.id'))

    # Query
    search_term = db.Column(db.Boolean,  nullable=False)

    # New instance instantiation procedure
    def __init__(self, search_id, search_term):

        self.search_id = search_id
        self.search_term = search_term

    def __repr__(self):
        return '<Artist Query: %r>' % (self.search_term)   

# Define a Recording Search model
class RecordingSearches(Base):

    __tablename__ = 'recording_search_queries'

    # Is artist search
    search_id = db.Column(db.Integer,  db.ForeignKey('search_data.id'))

    # Is recording search
    search_term = db.Column(db.Boolean,  nullable=False)

    # New instance instantiation procedure
    def __init__(self, search_id, search_term):

        self.search_id = search_id
        self.search_term = search_term


    def __repr__(self):
        return '<Recording Query: %r>' % (self.search_term)     

