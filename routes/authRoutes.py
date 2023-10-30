from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel
from typing import List, Annotated
from models import userModel as userM 
from database import SessionLocal, engine, UserBase
from sqlalchemy.orm import Session
from security import hasher as hash
from fastapi.responses import JSONResponse

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
    db_user = userM.Users(username="TESTTT",email=user.email,password=hashed_password,image=def_profile_img)
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