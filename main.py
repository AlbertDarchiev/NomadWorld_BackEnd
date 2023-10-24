from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from models import userModel as userM
from database import SessionLocal, engine, UserBase
from sqlalchemy.orm import Session
import uvicorn
#from routes import authRoutes
from routes import authRoutes as auth_router

app = FastAPI()
app.include_router(auth_router.router)

userM.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)