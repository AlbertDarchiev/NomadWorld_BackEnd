from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import SessionLocal, engine, UserBase
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
            
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/users", response_model=List[UserBase])
def get_users(db: db_dependency):
    users = db.query(models.User).all()
    return users

@app.get("/users/{user_id}", response_model=UserBase)
def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/register", response_model=UserBase)
def create_user(user:UserBase,db:db_dependency):
    db_user = models.User(username=user.username,email=user.email,password=user.password,image=user.image)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close(db_user)
    return db_user