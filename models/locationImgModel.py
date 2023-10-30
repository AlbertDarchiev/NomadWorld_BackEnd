from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base
from sqlalchemy.orm import relationship
class LocationImage(Base):
    __tablename__ = "location_image"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
