from sqlalchemy import Column, Integer, String, Date, ForeignKey, Double, DateTime, ARRAY, Float
from datetime import datetime

from database import Base

class Location_comment(Base):
    __tablename__ = "location_comment"
    comment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    location_id = Column(Integer, ForeignKey("location.id"))
    comment = Column(String)
    date = Column(String)