import base64
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel
from typing import List, Annotated, Optional
from models import userModel as userM 
from database import SessionLocal, engine, UserBase
from sqlalchemy.orm import Session
from security import hasher as hash
from fastapi.responses import JSONResponse
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from emailSender import sender as email

#userModel.Base.metadata.create_all(bind=engine)    

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
    users = db.query(userM.Users).all()
    return users

@router.get("/users/{user_id}")
def get_user(user_id: int, db: db_dependency):
    user = db.query(userM.Users).filter(userM.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register", response_model=UserBase)
def create_user(user:UserBase,db:db_dependency):
    if user.username == "":
        raise HTTPException(status_code=400, detail="Username is empty")
    db_username_exist = db.query(userM.Users).filter(userM.Users.username == user.username).first()
    if db_username_exist:
        raise HTTPException(status_code=404, detail="Username already exists")
    if user.email == "":
        raise HTTPException(status_code=400, detail="Email is empty")
    if user.password == "":
        raise HTTPException(status_code=400, detail="Password is empty")
    
    if not email.ESender.check(user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    
    hashed_password = hasher.get_password_hash(user.password)
    db_user = userM.Users(
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
def login(user:UserBase, db:db_dependency):
    if user.email == "":
        raise HTTPException(status_code=400, detail="Email is empty")
    
    db_user = db.query(userM.Users).filter(userM.Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not hasher.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return JSONResponse(status_code=200, content="User logged successfully")

@router.patch("/users/modify/{user_id}")
def update_user(user_id: int,db:db_dependency, username: Optional[str] = None, mail: Optional[str] = None):
    db_user = db.query(userM.Users).filter(userM.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if username is not None:
        db_username_exist = db.query(userM.Users).filter(userM.Users.username == username).first()
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

@router.patch("/users/modify_pass/{user_id}")
def change_pass(user_id: int, user:UserBase, db:db_dependency):
    db_user = db.query(userM.Users).filter(userM.Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User ID not found")
    db_user.password = hasher.get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    db.close()
    return JSONResponse(status_code=200, content="Password changed successfully")

@router.patch("/users/modify_image/{user_id}")
async def change_img(user_id: int, db:db_dependency, image_file: str):
    db_user = db.query(userM.Users).filter(userM.Users.id == user_id).first()
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