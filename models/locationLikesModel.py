from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Interval
from database import Base

class LocationLikes(Base):
    __tablename__ = "location_like"
    like_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    location_id = Column(Integer, ForeignKey("location.id"))