from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from models import userModel as userM
from database import SessionLocal, engine, UserBase
from sqlalchemy.orm import Session
from routes import authRoutes, mediaRoutes, imageRoutes
import uvicorn

app = FastAPI()
app.include_router(authRoutes.router, tags=['Authentication'])
app.include_router(authRoutes.routerUserP, tags=['User Params'])
app.include_router(mediaRoutes.routerLoc, tags=['Location Endpoints'])
app.include_router(mediaRoutes.router, tags=['Route Endpoints'])

app.include_router(mediaRoutes.routerExtra, tags=['EXTRA Features'])

#app.include_router(imageRoutes.router)

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')

#userM.Base.metadata.create_all(bind=engine)