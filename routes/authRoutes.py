import base64
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel
from typing import List, Annotated, Optional
from models import locationModel, userModel, imageModel, routeModel
from database import SessionLocal, engine, UserBase
from sqlalchemy.orm import Session
from security import hasher as hash
from fastapi.responses import JSONResponse
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from emailSender import sender as email
from password_generator import PasswordGenerator

#userModelodel.Base.metadata.create_all(bind=engine)    

hasher = hash.Hasher()
def_profile_img = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

router = APIRouter()
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/users", response_model=List[UserBase])
def get_users(db: db_dependency):
    users = db.query(userModel.Users).all()
    return users

@router.get("/users/{user_id}")
def get_user(user_id: int, db: db_dependency):
    user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register", response_model=UserBase)
def create_user(user:UserBase,db:db_dependency):
    if user.username == "":
        raise HTTPException(status_code=400, detail="Username is empty")
    db_username_exist = db.query(userModel.Users).filter(userModel.Users.username == user.username).first()
    db_email_exist = db.query(userModel.Users).filter(userModel.Users.email == user.email).first()
    if db_username_exist:
        raise HTTPException(status_code=404, detail="Username already exists")
    if user.email == "":
        raise HTTPException(status_code=400, detail="Email is empty")
    if db_email_exist:
        raise HTTPException(status_code=404, detail="Email already exists")
    if user.password == "":
        raise HTTPException(status_code=400, detail="Password is empty")
    
    if not email.ESender.check(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    
    hashed_password = hasher.get_password_hash(user.password)
    db_user = userModel.Users(
        username=user.username,
        email=user.email,
        password=hashed_password,
        img=def_profile_img, 
        saved_routes=[], 
        saved_locations=[])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()

    subject = '¡ Bienvenido a Nomad World !'
    body = f"Usuario, {db_user.username} creado correctamente"
    receiver = user.email
    email.ESender.send_email(receiver, subject, body)

    return JSONResponse( status_code=201, content="User created successfully")


@router.post("/login")
async def login(user:UserBase, db:db_dependency):
    if user.email == "":
        raise HTTPException(status_code=400, detail="Email is empty")

    db_user = db.query(userModel.Users).filter(userModel.Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not hasher.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    routes = []
    locations = []
    
    for route in db_user.saved_routes:
        route_locations = []
        db_route = db.query(routeModel.Route).filter(routeModel.Route.id == route).first()
        if db_route is not None:
            for loc_id in db_route.location_id:
                db_loc = db.query(locationModel.Location).filter(locationModel.Location.id == loc_id).first()
                if db_loc is not None:
                    db_image = db.query(imageModel.Image.image_uri).filter(imageModel.Image.id == db_loc.image_id).first()
                    if db_image is not None:
                        db_loc.image = db_image[0]
                    else:
                        db_loc.image = []
                    route_locations.append(db_loc)
        routes.append(db_route)

    for loc_id in db_user.saved_locations:
        db_loc = db.query(locationModel.Location).filter(locationModel.Location.id == loc_id).first()
        if db_loc is not None:
            db_image = db.query(imageModel.Image.image_uri).filter(imageModel.Image.id == db_loc.image_id).first()
            if db_image is not None:
                db_loc.image = db_image[0]
            else:
                db_loc.image = []
            locations.append(db_loc)
    
    db_user.saved_routes = routes
    db_user.saved_locations = locations
    return db_user



# USER PARAMS
router2 = APIRouter()

@router2.patch("/users/restore_pass/{user_id}")
def reset_pass(user_id: int, db:db_dependency):
    db_user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        pwo = PasswordGenerator()
        pwo.maxlen = 15
        pwo.minlen = 10
        newpass = pwo.generate()
        subject = f"Hola {db_user.username}, hemos restablecido tu contraseña"
        body = f"Esta es tu nueva contraseña: {newpass}"
        receiver = db_user.email
        #print(newpass)
        email.ESender.send_email(receiver, subject, body)

        db_user.password = hasher.get_password_hash(newpass)
        db.commit()
        db.refresh(db_user)
        db.close()
        return JSONResponse(status_code=200, content="Password restored successfully")

@router2.patch("/users/modify/{user_id}")
def update_user(user_id: int,db:db_dependency, username: Optional[str] = None, mail: Optional[str] = None):
    db_user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if username is not None:
        db_username_exist = db.query(userModel.Users).filter(userModel.Users.username == username).first()
        if db_username_exist:
            raise HTTPException(status_code=404, detail="Username already exists")
        else:
            db_user.username = username
    if mail is not None:
        if not email.ESender.check(mail):
            raise HTTPException(status_code=400, detail="Invalid email")
        else:
            db_user.email = mail
    db.commit()
    db.refresh(db_user)
    db.close()
    return JSONResponse(status_code=200, content="User updated successfully")

@router2.patch("/users/modify_pass/{user_id}")
def change_pass(user_id: int, current_pass: str, new_pass: str, db:db_dependency):
    db_user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User ID not found")
    if not hasher.verify_password(current_pass, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    else:
        db_user.password = hasher.get_password_hash(new_pass)
        db.commit()
        db.refresh(db_user)
        db.close()
        return JSONResponse(status_code=200, content="Password changed successfully")

@router2.patch("/users/modify_image/{user_id}")
async def change_img(user_id: int, db:db_dependency, image_file: str):
    db_user = db.query(userModel.Users).filter(userModel.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User ID not found")
    image_name = f"image_user_{user_id}.png"
    await upload_file("profile_images", image_name, image_file)
    db_user.img = f"https://ik.imagekit.io/albertITB/profile_images/{image_name}"
    db.commit()
    db.refresh(db_user)
    db.close()
    return JSONResponse(status_code=200, content="Image changed successfully")

async def upload_file(foldername: str, image_name:str, file: base64):
    imagekit = ImageKit(
        private_key='private_iDHFe+AfM2FSVeBe1o11jqllHB4=',
        public_key='public_SWebOtYLMFIFinKilKGXkwGFAoM=',
        url_endpoint='https://ik.imagekit.io/albertITB'
    )

    imagekit.upload(
        file,
        file_name=image_name,
        options=UploadFileRequestOptions( 
            use_unique_file_name=False,
            folder=foldername
        ))