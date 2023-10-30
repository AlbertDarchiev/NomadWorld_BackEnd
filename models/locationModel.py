from sqlalchemy import Column, Integer, String, ForeignKey, Double, Date
from database import Base

class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    latitude = Column(Double)
    longitude = Column(Double)
    created_at = Column(Date)
    country_id = Column(Integer, ForeignKey("Country.id"))