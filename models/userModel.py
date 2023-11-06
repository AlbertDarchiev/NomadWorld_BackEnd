from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, ARRAY
from database import Base

class Users(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    img = Column(String)
    saved_routes = Column(ARRAY(Integer))
    saved_locations = Column(ARRAY(Integer))
