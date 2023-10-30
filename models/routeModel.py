from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Interval
from database import Base

class Route(Base):
    __tablename__ = "route"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    distance = Column(String)
    duration = Column(Interval)
    location_id = Column(Integer, ForeignKey("Location.id"))
