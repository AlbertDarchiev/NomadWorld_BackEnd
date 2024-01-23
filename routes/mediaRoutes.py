import copy
from fastapi import FastAPI, HTTPException, Depends, APIRouter, File, Form, UploadFile
from database import SessionLocal, engine, UserBase, RouteBase, LocationBase, ImageBase, LocationCommentBase, LocationLikeBase, RouteCommentBase
import models 
from typing import List, Annotated, Union
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, select
from models import routeModel as routeM
from models import userModel, locationModel, imageModel, coutryModel, routeLikesModel, locationLikesModel, routeModel, locationCommentModel,routeCommentModel
from datetime import datetime
import base64
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()
routerLoc = APIRouter()

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

# SAVE LOCATION --------------------------------------------------------------------
@routerLoc.patch("/save/location/")
def save_location(db: db_dependency, user_id : int, location_id: int):
    user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()
    location = db.query(locationModel.Location).filter(locationModel.Location.id == location_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User id not found")
    elif not location:
        raise HTTPException(status_code=404, detail="Location id not found")
    elif location_id in user.saved_locations:
        raise HTTPException(status_code=404, detail="Location already saved")
    else:
        new_data = copy.copy(user.saved_locations)
        new_data.append(location_id)
        user.saved_locations = new_data
        db.commit()
        db.refresh(user)
        return user
    
# SAVE ROUTE --------------------------------------------------------------------
@router.patch("/save/route/")
def save_location(db: db_dependency, user_id : int, route_id: int):
    route = db.query(routeModel.Route).filter(routeModel.Route.id == route_id).first()
    user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route id not found")
    elif not user:
        raise HTTPException(status_code=404, detail="User id not found")
    elif route_id in user.saved_routes:
        raise HTTPException(status_code=404, detail="Route already saved")
    else :
        new_data = copy.copy(user.saved_routes)
        new_data.append(route_id)
        user.saved_routes = new_data
        db.commit()
        db.refresh(user)
        return user
    
# UNSAVE LOCATION --------------------------------------------------------------------
@routerLoc.patch("/unsave/location/")
def save_location(db: db_dependency, user_id : int, location_id: int):
    location = db.query(locationModel.Location).filter(locationModel.Location.id == location_id).first()
    user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location id not found")
    elif not user:
        raise HTTPException(status_code=404, detail="User id not found")
    elif location_id not in user.saved_locations:
        raise HTTPException(status_code=404, detail="Location already unsaved")
    else :
        new_data = copy.copy(user.saved_locations)
        new_data.remove(location_id)
        user.saved_locations = new_data
        db.commit()
        db.refresh(user)
        return user

# UNSAVE ROUTE --------------------------------------------------------------------
@router.patch("/unsave/route/")
def unsave_route(db: db_dependency, user_id : int, route_id: int):
    route = db.query(routeModel.Route).filter(routeModel.Route.id == route_id).first()
    user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()

    if not route:
        raise HTTPException(status_code=404, detail="Route id not found")
    elif not user:
        raise HTTPException(status_code=404, detail="User id not found")
    elif route_id not in user.saved_routes:
        raise HTTPException(status_code=404, detail="Route already unsaved")
    else :
        new_data = copy.copy(user.saved_routes)
        new_data.remove(route_id)
        user.saved_routes = new_data
        db.commit()
        db.refresh(user)
        return user

# ROUTE ROUTES ---------------------------------------------------------------------
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
        responses.append(route)
    return responses

@router.get("/route/")    
def get_media_route(db: db_dependency):
    route_info = db.query(routeModel.Route).all()
    responses = []
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    for route in route_info:
        locations = []
        for i, loc_id in enumerate(route.location_id):
            location = db.query(locationModel.Location).filter(locationModel.Location.id == loc_id).first()
            if location is not None:
                image = db.query(imageModel.Image).filter(imageModel.Image.id == location.image_id).first()
                if image is not None:
                    location.image = image.image_uri
                    locations.append(location)
                else:
                    print(f"Image not found for location {location.id}")
            else:
                print(f"Location not found for route {route.id}, location_id: {loc_id}")
        route.location_id = locations
        responses.append(route)
    
    return responses


@router.get("/route/{country_name}")
def get_route_by_country_route(country_name: str, db: db_dependency):
    country = db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not foundd")
    
    route_info = db.query(routeM.Route).filter(routeModel.Route.country_id == country.id).all()
    responses = []
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    for route in route_info:
        locations = []
        for i, loc_id in enumerate(route.location_id):
            location = db.query(locationModel.Location).filter(locationModel.Location.id == loc_id).first()
            if location is not None:
                image = db.query(imageModel.Image).filter(imageModel.Image.id == location.image_id).first()
                if image is not None:
                    location.image = image.image_uri
                    locations.append(location)
                else:
                    print(f"Image not found for location {location.id}")
            else:        
                print(f"Location not found for route {route.id}, location_id: {loc_id}")
        route.location_id = locations
        responses.append(route)
    
    return responses

@router.post("/create_route/{country_name}", response_model=RouteBase)
def create_route_route(country_name: str, route: RouteBase, db: db_dependency):
    country_name = db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first().id
    db_route = routeM.Route(
        name=route.name,
        description=route.description,
        distance=route.distance,
        duration=route.duration,
        country_id=country_name,
        location_id=route.location_id
        )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

@router.post("/save_route", response_model=RouteBase)
def save_route(db:db_dependency, country_name:str, route: RouteBase = Depends()):
    db_route = routeModel.Route(
        name = route.name,
        descirption = route.description,
        distance = route.distance,
        duration = route.duration,
        country_id = db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first().id,
        location_id = route.location_id
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


# LOCATION ROUTES ---------------------------------------------------------------------

@routerLoc.get("/location")
def get_location(db: db_dependency): 
    location_info = db.query(locationModel.Location).all()
    responses = []
    if not location_info:
        raise HTTPException(status_code=404, detail="Location not found")
    
    for loc in location_info:
        db_image = db.query(imageModel.Image.image_uri).filter(imageModel.Image.id == loc.image_id).first()
        if db_image is not None:
            loc.image = db_image[0]
        else:
            loc.image = []
        responses.append(loc)
    return responses

@routerLoc.get("/location/{country_name}")
def get_location_route(country_name:str, db: db_dependency):
    country = db.query(coutryModel.Country).filter(coutryModel.Country.name == country_name).first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not foundasdasdsad")

    location_info = db.query(locationModel.Location).filter(locationModel.Location.country_id == country.id).all()
    responses = []
    if not location_info:
        raise HTTPException(status_code=404, detail="Location not found")

    for loc in location_info:
        db_image = db.query(imageModel.Image.image_uri).filter(imageModel.Image.id == loc.image_id).first()
        if db_image is not None:
            loc.image = db_image[0]
        else:
            loc.image = []
        responses.append(loc)
    return responses

@routerLoc.get("/location/id/{loc_id}")
def get_location_by_id(loc_id:int, db: db_dependency):
    location_info = db.query(locationModel.Location).filter(locationModel.Location.id == loc_id).first()
    
    responses = []
    if location_info is None:
        raise HTTPException(status_code=404, detail="Location not found")
    else:
        image = db.query(imageModel.Image).filter(imageModel.Image.id == location_info.image_id).first().image_uri
        if image is not None:
            location_info.image = image
        else:
            location_info.image = []
        responses.append(location_info)
    return responses

@routerLoc.post("/create_location/{country_name}", response_model=LocationBase)
async def create_location_location( country_name: str, db: db_dependency, image_files: List[str], location: LocationBase):
    
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

#Comment location
@routerLoc.post("/add_comment/location", response_model=LocationCommentBase)
def create_location_location( db: db_dependency, comment: LocationCommentBase):
    date_now = datetime.now()
    loc_id_exists = db.query(locationModel.Location).filter(locationModel.Location.id == comment.location_id).first()
    if not loc_id_exists:
        raise HTTPException(status_code=404, detail="Location id not found")

    db_comment = locationCommentModel.Location_comment(
        user_id = comment.user_id,
        location_id = comment.location_id,
        comment = comment.comment,
        date = date_now
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    db.close()
    return JSONResponse( status_code=201, content="Comment posted successfully")

@routerLoc.get("/comment/location/{loc_id}")
def get_comment_location(loc_id:int, db: db_dependency):
    location_info = db.query(locationModel.Location).filter(locationModel.Location.id == loc_id).first()
    if not location_info:
        raise HTTPException(status_code=404, detail="Location not found")
    else:
        comments = db.query(locationCommentModel.Location_comment).filter(locationCommentModel.Location_comment.location_id == loc_id).all()
        if not comments:
            raise HTTPException(status_code=404, detail="Comments not found")
        else:
            return comments
#COMMENT ROUTE´
@router.post("/add_comment/route", response_model=RouteCommentBase)
def create_route_comment(db: db_dependency, comment: RouteCommentBase):
    date_now = datetime.now()
    route_id_exists = db.query(routeModel.Route).filter(routeModel.Route.id == comment.route_id).first()
    if not route_id_exists:
        raise HTTPException(status_code=404, detail="Route id not found")

    db_comment = routeCommentModel.Route_comment(
        user_id = comment.user_id,
        route_id = comment.route_id,
        comment = comment.comment,
        date = date_now
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    db.close()
    return JSONResponse( status_code=201, content="Comment posted successfully")

@router.get("/comment/route/{route_id}")
def get_comment_route(route_id:int, db: db_dependency):
    route_info = db.query(routeModel.Route).filter(routeModel.Route.id == route_id).first()
    if not route_info:
        raise HTTPException(status_code=404, detail="Route not found")
    else:
        comments = db.query(routeCommentModel.Route_comment).filter(routeCommentModel.Route_comment.route_id == route_id).all()
        if not comments:
            raise HTTPException(status_code=404, detail="Comments not found")
        else:
            return comments

@routerLoc.delete("/delete_location_comment/{comment_id}")
def delete_comment(comment_id: int, db: db_dependency):
    comment = db.query(locationCommentModel.Location_comment).filter(locationCommentModel.Location_comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    else:
        db.delete(comment)
        db.commit()
        return JSONResponse( status_code=201, content="Comment deleted successfully")

@router.delete("/delete_route_comment/{comment_id}")
def delete_comment(comment_id: int, db: db_dependency):
    comment = db.query(routeCommentModel.Route_comment).filter(routeCommentModel.Route_comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    else:
        db.delete(comment)
        db.commit()
        return JSONResponse( status_code=201, content="Comment deleted successfully")
    
#LIKES LOCATION       
@routerLoc.post("/like/location/")
def like_location(user_id: int, loc_id:int, db: db_dependency):
    if not db.query(userModel.Users).filter(userModel.Users.id == user_id).first():
        raise HTTPException(status_code=400, detail="User ID not found")
    if not db.query(locationModel.Location).filter(locationModel.Location.id == loc_id).first():
        raise HTTPException(status_code=400, detail="Location ID not found")
    if db.query(locationLikesModel.LocationLikes).filter(locationLikesModel.LocationLikes.user_id == user_id).filter(locationLikesModel.LocationLikes.location_id == loc_id).first():
        raise HTTPException(status_code=400, detail="Already liked")

    db_like = locationLikesModel.LocationLikes(
        user_id = user_id,
        location_id = loc_id
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    db.close()
    return JSONResponse( status_code=201, content="Location liked successfully")

@routerLoc.delete("/unlike/location/")
def unlike_location(user_id: int, loc_id:int, db: db_dependency):
    if not db.query(userModel.Users).filter(userModel.Users.id == user_id).first():
        raise HTTPException(status_code=400, detail="User ID not found")
    if not db.query(locationModel.Location).filter(locationModel.Location.id == loc_id).first():
        raise HTTPException(status_code=400, detail="Location ID not found")
    db_like = db.query(locationLikesModel.LocationLikes).filter(locationLikesModel.LocationLikes.user_id == user_id).filter(locationLikesModel.LocationLikes.location_id == loc_id).first()
    if not db_like:
        raise HTTPException(status_code=400, detail="Like not found")
    db.delete(db_like)
    db.commit()
    db.close()
    return JSONResponse( status_code=201, content="Location unliked successfully")

@routerLoc.get("/likes/location/{loc_id}")
def get_loc_likes(loc_id:int,  db: db_dependency):
    loc_Model = locationLikesModel.LocationLikes
    liked_loc = db.query(loc_Model).filter(loc_Model.location_id == loc_id).all()
    if not liked_loc:
        raise HTTPException(status_code=400, detail="Likes not found")
    else:
        return liked_loc

#LIKES ROUTE       
@router.post("/like/route/")
def like_route(user_id: int, route_id:int, db: db_dependency):
    if not db.query(userModel.Users).filter(userModel.Users.id == user_id).first():
        raise HTTPException(status_code=400, detail="User ID not found")
    if not db.query(routeModel.Route).filter(routeModel.Route.id == route_id).first():
        raise HTTPException(status_code=400, detail="Route ID not found")
    if db.query(routeLikesModel.RouteLikes).filter(routeLikesModel.RouteLikes.user_id == user_id).filter(routeLikesModel.RouteLikes.route_id == route_id).first():
        raise HTTPException(status_code=400, detail="Already liked")

    db_like = routeLikesModel.RouteLikes(
        user_id = user_id,
        route_id = route_id
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    db.close()
    return JSONResponse( status_code=201, content="Route liked successfully")

@router.delete("/unlike/route/")
def unlike_route(user_id: int, route_id:int, db: db_dependency):
    if not db.query(userModel.Users).filter(userModel.Users.id == user_id).first():
        raise HTTPException(status_code=400, detail="User ID not found")
    if not db.query(routeModel.Route).filter(routeModel.Route.id == route_id).first():
        raise HTTPException(status_code=400, detail="Route ID not found")
    db_like = db.query(routeLikesModel.RouteLikes).filter(routeLikesModel.RouteLikes.user_id == user_id).filter(routeLikesModel.RouteLikes.route_id == route_id).first()
    if not db_like:
        raise HTTPException(status_code=400, detail="Like not found")
    db.delete(db_like)
    db.commit()
    db.close()
    return JSONResponse( status_code=201, content="Route unliked successfully")

@router.get("/likes/route/{route_id}")
def get_lroute_likes(route_id:int,  db: db_dependency):
    route_Model = routeLikesModel.RouteLikes
    liked_route = db.query(route_Model).filter(route_Model.location_id == route_id).all()
    if not liked_route:
        raise HTTPException(status_code=400, detail="Likes not found")
    else:
        return liked_route

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