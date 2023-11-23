from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Interval
from database import Base

class RouteLikes(Base):
    __tablename__ = "route_like"
    like_id: Column(int, nullable=True)
    user_id: Column(int, nullable=True)
    route_id: Column(int, nullable=True)

