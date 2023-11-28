from fastapi import FastAPI, HTTPException, Depends, APIRouter, File, Form, UploadFile
from database import SessionLocal, engine, UserBase, RouteBase, LocationBase, ImageBase
import models 
from typing import List, Annotated, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, select
from models import routeModel as routeM
from models import locationModel, imageModel, coutryModel, routeLikesModel, routeModel
from datetime import datetime
import base64
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from fastapi.responses import JSONResponse

from pydantic import BaseModel
router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/country/")
def get_country_route(db: db_dependency):
    country_info = db.query(coutryModel.Country).all()
    if not country_info:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_info

@router.get("/route/more_likes/")
def get_media_more_likes_route(db: db_dependency):
    route_info = db.query(routeModel.Route).join(routeLikesModel.RouteLikes).group_by(routeModel.Route.id).order_by(func.count(routeLikesModel.RouteLikes.route_id).desc()).all()
    responses = []
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    for route in route_info:
        print(route.location_id)
        locations = []
        for i, loc in enumerate(route.location_id):
            location = db.query(locationModel.Location).filter(locationModel.Location.id == route.location_id[i]).first()
            image = db.query(imageModel.Image).filter(imageModel.Image.id == location.image_id).first()
            location.image = image.image_uri
            locations.append(location)
        route.location_id = locations
        responses.append([route])
    return responses


@router.get("/route")    
def get_media_route(db: db_dependency):
    route_info = db.query(routeModel.Route).all()
    responses = []
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    for route in route_info:
        locations = []
        for i, loc in enumerate(route.location_id):
            location = db.query(locationModel.Location).filter(locationModel.Location.id == route.location_id[i]).first()
            image = db.query(imageModel.Image).filter(imageModel.Image.id == location.image_id).first()
            location.image = image.image_uri
            locations.append(location)
        route.location_id = locations
        responses.append([route])
    return responses

@router.get("/route/{country_name}")
def get_route_by_country_route(country_name: str, db: db_dependency):
    route_info = db.query(routeM.Route).filter(models.Route.country_name == country_name).all()
    responses = []
    for route in route_info:
        locations = []
        for i, loc in enumerate(route.location_id):
            location = db.query(locationModel.Location).filter(locationModel.Location.id == route.location_id[i]).first()
            image = db.query(imageModel.Image).filter(imageModel.Image.id == location.image_id).first()
            location.image = image.image_uri
            locations.append(location)
        route.location_id = locations
        responses.append([route])
    return route_info



@router.get("/location")
def get_location_route(db: db_dependency): 
    location_info = db.query(locationModel.Location).all()
    images = db.query(imageModel.Image).filter(imageModel.Image.id == locationModel.Location.image_id).all()
    
    responses = []
    if not location_info:
        raise HTTPException(status_code=404, detail="Location not found")
    for i, response in enumerate(location_info):
        responses.append([response, images[i]])
    return responses

@router.get("/location/{country_name}")
def get_location_route(country_name:str, db: db_dependency):
    location_info = db.query(locationModel.Location).filter(locationModel.Location.country_id == db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first().id).all()
    images = db.query(imageModel.Image).filter(imageModel.Image.id == locationModel.Location.image_id).all()
    
    responses = []
    if not location_info:
        raise HTTPException(status_code=404, detail="Location not found")
    for i, response in enumerate(location_info):
        responses.append([response, images[i]])
    return responses


@router.post("/create_location", response_model=LocationBase)
async def create_location_location( country_name: str, db: db_dependency, image_files: List[str], location: LocationBase = Depends()):
    
    loc_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db_location = locationModel.Location(
        name = location.name,
        description = location.description,
        creation_date=loc_date,
        country_id=db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first().id,
        longitude = location.longitude,
        latitude = location.latitude
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    list_images_name = []
    # https://ik.imagekit.io/albertITB/locationImg/$[datetime.now()]
    for i, image in enumerate(image_files):
        date = str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
        #img_ext = image.filename.split(".")[1]
        list_images_name.append(f"https://ik.imagekit.io/albertITB/locationImg/{date}.png")
        image_name = f"{date}.png"
        await upload_file("locationImg" ,image_name , image)

    loc_id = db.query(locationModel.Location).filter(locationModel.Location.creation_date == loc_date).first().id
    db_image = imageModel.Image(
        location_id=loc_id,
        image_uri=list_images_name
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    db.query(locationModel.Location).filter_by(creation_date=loc_date).update(
        {
        locationModel.Location.image_id: db_image.id,
        })
    
    db.commit()
    db.refresh(db_location)
    return JSONResponse( status_code=201, content="Location created successfully")



@router.post("/create_route/{country_name}", response_model=RouteBase)
def create_route_route(country_name: int, route: RouteBase, db: db_dependency):
    country_name = db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first().id
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

async def upload_file(foldername: str, image_name:str, file: base64):
    imagekit = ImageKit(
        private_key='private_iDHFe+AfM2FSVeBe1o11jqllHB4=',
        public_key='public_SWebOtYLMFIFinKilKGXkwGFAoM=',
        url_endpoint='https://ik.imagekit.io/albertITB'
    )
    #content = await file
    #image_base64 = base64.b64encode(content).decode("utf-8")

    imagekit.upload(
        file, #se especifica el archivo a subir
        file_name=image_name, #se especifica el nombre del archivo
        options=UploadFileRequestOptions( #se especifican las opciones de subida(con las que hay ahora tenemos suficiente)
            use_unique_file_name=False,
            folder=foldername
        ))