from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user_accounts'
    u_id = Column(Integer, primary_key=True)
    username = Column(String(40), unique=True)

        # New instance instantiation procedure
    def __init__(self, u_id, username):

        self.u_id = u_id
        self.username = username
