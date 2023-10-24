from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base

class Location(Base):
    __tablename__ = "Location"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("User.id"))
    description = Column(Text)
    like = Column(Integer)