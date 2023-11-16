from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, ARRAY
from database import Base

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(String, nullable=True)
    image_uri = Column(ARRAY(String), nullable=True)
