from fastapi import FastAPI, HTTPException, Depends, APIRouter
from database import SessionLocal, engine, UserBase
import models


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
    route_info = db.query(models.Route).order_by(models.Route.like.desc()).all()
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    # Retornar todas las rutas ordenadas por likes en orden descendente
    return route_info
    
@router.get("/route/")    
def get_media_route(db: db_dependency):
    route_info = db.query(models.Route).all()
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    return route_info

@router.get("/route/{country_id}")
def get_route_by_country_route(country_id: int, db: db_dependency):
    route_info = db.query(models.Route).filter(models.Route.country_id == country_id).all()
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    # Retornar todas las rutas ordenadas por likes en orden descendente
    return route_info

@router.get("/location/")
def get_location_route(db: db_dependency): 
    location_info = db.query(models.Location).all()
    if not location_info:
        raise HTTPException(status_code=404, detail="Location not found")
    return location_info

@router.get("/country/")
def get_country_route(db: db_dependency):
    country_info = db.query(models.Country).all()
    if not country_info:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_info


@router.post("/create_route/")
def create_route_route(route: models.Route, db: db_dependency):
    db_route = models.Route(name=route.name, description=route.description, like=route.like, country_id=route.country_id)
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    db.close()
    return db_route
