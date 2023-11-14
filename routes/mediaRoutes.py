from fastapi import FastAPI, HTTPException, Depends, APIRouter, File, UploadFile
from database import SessionLocal, engine, UserBase, RouteBase, LocationBase, ImageBase
import models 
from typing import List, Annotated
from sqlalchemy.orm import Session
from models import routeModel as routeM
from models import locationModel, imageModel, coutryModel
from datetime import datetime
import base64
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

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

@router.post("/createimg", response_model=LocationBase)

def create_image(location: LocationBase,  db: db_dependency, image_files: List[UploadFile] = File(...)):
    loc_date = str(datetime.now())
    
    db_location = locationModel.Location(
        creation_date=loc_date
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.post("/create_location/{country_name}", response_model=LocationBase)
def create_location_route(country_name: str, image: ImageBase, location: LocationBase,  db: db_dependency, image_files: List[UploadFile] = File(...)):
    loc_date = str(datetime.now())
    db_location = locationModel.Location(
        creation_date=loc_date
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    list_images_name = []
    # https://ik.imagekit.io/albertITB/locationImg/$[datetime.now()]
    for i, image in enumerate(image_files):    
        list_images_name.append(str(datetime.now()))
        upload_file("locationImg",list_images_name[i] , image)

    list_images_uri = []
    for i in list_images_name:
        img_ext = image_files[i].filename.split(".")[1]
        list_images_uri.append(f"https://ik.imagekit.io/albertITB/locationImg/{i}.{img_ext}")

    loc_id = db.query(locationModel.Location).filter(locationModel.Location.creation_date == loc_date).first().id
    db_image = imageModel.Image(
        location_id=loc_id,
        image_uri=list_images_uri
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    db.query(locationModel.Location).filter_by(creation_date=loc_date).update(
        {locationModel.Location.name: location.name,
        locationModel.Location.description: location.description,
        locationModel.Location.country_id: db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first().id,
        locationModel.Location.image_id: db_image.id,
        locationModel.Location.longitude: location.longitude,
        locationModel.Location.latitude: location.latitude})
    
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

async def upload_file(foldername: str, image_name:str, file: UploadFile = File(...)):
    imagekit = ImageKit(
        private_key='private_iDHFe+AfM2FSVeBe1o11jqllHB4=',
        public_key='public_SWebOtYLMFIFinKilKGXkwGFAoM=',
        url_endpoint='https://ik.imagekit.io/albertITB'
    )
    content = await file.read()
    image_base64 = base64.b64encode(content).decode("utf-8")

    upload_file = imagekit.upload(
        file = image_base64, #se especifica el archivo a subir
        file_name=image_name, #se especifica el nombre del archivo
        options=UploadFileRequestOptions( #se especifican las opciones de subida(con las que hay ahora tenemos suficiente)
            use_unique_file_name=False,
            folder=foldername
        ))