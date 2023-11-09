from sqlalchemy import Column, Integer, String, ForeignKey, Double, DateTime, ARRAY, Float
from database import Base


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    creation_date  = Column(DateTime(timezone=True))
    country_id = Column(Integer, ForeignKey("Country.id"))
    image_id = Column(Integer, ForeignKey("Image.id"))
    longitude = Column(Float)
    latitude = Column(Float)
