from sqlalchemy import Column, Integer, String, Date, ForeignKey, Double, DateTime, ARRAY, Float
from datetime import datetime

from database import Base

class Route_comment(Base):
    __tablename__ = "route_comment"
    comment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    route_id = Column(Integer, ForeignKey("route.id"))
    comment = Column(String)
    date = Column(String)