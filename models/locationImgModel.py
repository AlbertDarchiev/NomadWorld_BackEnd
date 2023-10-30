from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base
<<<<<<< HEAD
from sqlalchemy.orm import relationship
=======

>>>>>>> 36050c65bf0dde376e65b48abb4b28fb099d16c2
class LocationImage(Base):
    __tablename__ = "location_image"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
