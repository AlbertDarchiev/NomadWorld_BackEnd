import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List

URL_DATABASE = "postgresql://fl0user:bIqOB7Q5XrTi@ep-wild-snow-33454215.eu-central-1.aws.neon.fl0.io:5432/nomadworld?sslmode=require"
#"postgresql://fl0user:Kj7obcqEh3LZ@ep-holy-breeze-83855958.eu-central-1.aws.neon.fl0.io:5432/database?sslmode=require"
#"postgresql://fl0user:bIqOB7Q5XrTi@ep-wild-snow-33454215.eu-central-1.aws.neon.fl0.io:5432/nomadworld?sslmode=require"
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  

Base = declarative_base()

class UserBase(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email:str
    password: str
    img: Optional[str] = None
    saved_routes: Optional[List[int]] = None
    saved_locations: Optional[List[int]] = None

class RouteBase(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    distance: int
    duration: int
    country_id: Optional[int] = None
    location_id: List[int]

class LocationBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[str] = None
    country_id: Optional[int] = None
    image_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ImageBase(BaseModel):
    id: Optional[int] = None
    location_id: Optional[int] = None
    image_uri: List[str]

class RouteLikesBase(BaseModel):
    like_id: Optional[int] = None
    user_id: Optional[int] = None
    route_id: Optional[int] = None

class RouteCommentBase(BaseModel):
    comment_id: Optional[int] = None
    user_id: int
    route_id: int
    comment: str
    date: str

class LocationLikeBase(BaseModel):
    like_id: Optional[int] = None
    user_id: Optional[int] = None
    route_id: Optional[int] = None

class LocationCommentBase(BaseModel):
    comment_id: Optional[int] = None
    user_id: int
    location_id: int
    comment: str
    date: Optional[str] = None