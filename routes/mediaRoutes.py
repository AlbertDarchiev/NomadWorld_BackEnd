from fastapi import FastAPI, HTTPException, Depends, APIRouter
from database import SessionLocal, engine, UserBase, RouteBase, LocationBase, ImageBase
import models 
from typing import List, Annotated
from sqlalchemy.orm import Session
from models import routeModel as routeM
from models import locationModel, imageModel, coutryModel
from datetime import datetime

from pydantic import BaseModel
router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/route/more_likes/")
def get_media_more_likes_route(db: db_dependency):
    route_info = db.query(routeM.Route).order_by(models.Route.like.desc()).all()

    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    # Retornar todas las rutas ordenadas por likes en orden descendente
    return route_info
    
@router.get("/route/")    
def get_media_route(db: db_dependency):
    route_info = db.query(routeM.Route).all()

    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    return route_info

@router.get("/route/{country_id}")
def get_route_by_country_route(country_id: int, db: db_dependency):
    route_info = db.query(routeM.Route).filter(models.Route.country_id == country_id).all()
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    # Retornar todas las rutas ordenadas por likes en orden descendente
    return route_info

@router.get("/location/")
def get_location_route(db: db_dependency): 
    location_info = db.query(locationModel.Location).all()
    images = db.query(imageModel.Image).filter(imageModel.Image.id == locationModel.Location.image_id).all()
    

    if not location_info:
        raise HTTPException(status_code=404, detail="Location not found")
    return [location_info, images]

@router.post("/create_location/{country_name}", response_model=LocationBase)
def create_location_route(country_name:str, location: LocationBase, db: db_dependency):
    country_id = db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first().id
    db_location = locationModel.Location(
        name=location.name,
        description=location.description,
        creation_date=datetime.now(),
        country_id=country_id,
        image_id=location.image_id,
        latitude=location.latitude,
        longitude=location.longitude
        )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.get("/country/")
def get_country_route(db: db_dependency):
    country_info = db.query(coutryModel.Country).all()
    if not country_info:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_info


@router.post("/create_route", response_model=RouteBase)

def create_route_route(country_name: int, route: RouteBase, db: db_dependency):
    country_id = db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first().id
    db_route = routeM.Route(
        name=route.name,
        description=route.description,
        distance=route.distance,
        duration=route.duration,
        location_id=route.location_id
        
        )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route