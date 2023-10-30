from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_url = Column(String)
