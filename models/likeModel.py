from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base
from sqlalchemy.orm import relationship

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location")
    route_id = Column(Integer, ForeignKey("route.id"))
    route = Relationship("Route")
    created_at = Column(DateTime(timezone=True))