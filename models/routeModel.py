from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Interval, ARRAY
from database import Base

class Route(Base):
    __tablename__ = "route"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    distance = Column(Integer)
    duration = Column(Integer)
    country_id = Column(Integer, ForeignKey("country.id"))
    location_id = Column(ARRAY(Integer))
    #location_id = Column(Integer, ForeignKey("location.id"))