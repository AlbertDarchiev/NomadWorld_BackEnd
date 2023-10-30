from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base
<<<<<<< HEAD
from sqlalchemy.orm import relationship
=======
>>>>>>> 36050c65bf0dde376e65b48abb4b28fb099d16c2

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location")
    route_id = Column(Integer, ForeignKey("route.id"))
<<<<<<< HEAD
    route = Relationship("Route")
=======
    route = relationship("Route")
>>>>>>> 36050c65bf0dde376e65b48abb4b28fb099d16c2
    created_at = Column(DateTime(timezone=True))