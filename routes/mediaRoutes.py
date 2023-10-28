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

@router.get("/media/more_likes/")
def get_media_more_likes_route(db: db_dependency):
    # Consulta en la base de datos utilizando SQLAlchemy
    route_info = db.query(models.Route).order_by(models.Route.like.desc()).all()
    # Verificar si hay resultados
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    # Retornar todas las rutas ordenadas por likes en orden descendente
    return route_info
    
@router.get("/media/")    
def get_media_route(db: db_dependency):
    # Consulta en la base de datos utilizando SQLAlchemy
    route_info = db.query(models.Route).all()
    # Verificar si hay resultados
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    # Retornar todas las rutas ordenadas por likes en orden descendente
    return route_info
    
