from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Interval
from database import Base

class RouteLikes(Base):
    __tablename__ = "route_like"
    like_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    route_id = Column(Integer, ForeignKey("route.id"))

