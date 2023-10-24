from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from database import Base

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    image = Column(String)
    
class Location(Base):
    __tablename__ = "Location"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("User.id"))
    description = Column(Text)
    like = Column(Integer)

class LocationImage(Base):
    __tablename__ = "LocationImage"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("Location.id"))
    image_url = Column(String)

class Route(Base):
    __tablename__ = "Route"
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("User.id"))
    title = Column(String)
    description = Column(Text)
    creationdate = Column(Date)
    like = Column(Integer)

class RouteImage(Base):
    __tablename__ = "RouteImage"
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("Route.id"))
    image_url = Column(String)

class Comment(Base):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(Integer, ForeignKey("User.id"))
    route = Column(Integer, ForeignKey("Route.id"))
    location = Column(Integer, ForeignKey("Location.id"))
    description = Column(Text)
    creationdate = Column(Date)

class UserSavedLocations(Base):
    __tablename__ = "UserSavedLocations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    location_id = Column(Integer, ForeignKey("Location.id"))

class UserSavedRoutes(Base):
    __tablename__ = "UserSavedRoutes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    route_id = Column(Integer, ForeignKey("Route.id"))