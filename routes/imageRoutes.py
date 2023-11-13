from fastapi import FastAPI, HTTPException, Depends, APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import httpx
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine, UserBase, RouteBase
from base64 import b64encode
from datetime import datetime
import aiohttp
import base64
import hmac
import hashlib
from fastapi.security import OAuth2PasswordBearer


from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from imagekitio import ImageKit
from imagekitio.models.CreateFolderRequestOptions import CreateFolderRequestOptions
router = APIRouter()


imagekit = ImageKit(
    private_key='private_iDHFe+AfM2FSVeBe1o11jqllHB4=',
    public_key='public_SWebOtYLMFIFinKilKGXkwGFAoM=',
    url_endpoint='https://ik.imagekit.io/albertITB'
)

auth_params = imagekit.get_authentication_parameters()
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 
db_dependency = Annotated[Session, Depends(get_db)]

print("Auth params-", auth_params)


@router.post("/upload/image")
async def upload_image(foldername: str, file: UploadFile = File(...)):
    #image_url = 'https://a.cdn-hotels.com/gdcs/production81/d1983/1441d9b5-d0e6-4230-9923-646d58ba66d8.jpg'
    
    content = await file.read()
    image_base64 = base64.b64encode(content).decode("utf-8")

    upload_file = imagekit.upload(
        file = image_base64,
        file_name=str(datetime.now()),
        options=UploadFileRequestOptions(
            use_unique_file_name=False,
            folder=foldername
        )
    )
    
    #create_folder = imagekit.create_folder(options=CreateFolderRequestOptions(folder_name="test", parent_folder_path="/"))
    #print("Create folder-", create_folder, end="\n\n")

    # Raw Response
    return upload_file.response_metadata.raw