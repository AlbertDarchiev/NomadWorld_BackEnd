from fastapi import FastAPI, HTTPException, Depends, APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine, UserBase, RouteBase
from base64 import b64encode
from datetime import datetime
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
# v la var "file" es lo que se envia desde el front (imagen)
# v la var "foldername" es el nombre de la carpeta donde se va a guardar la imagen
async def upload_image(foldername: str, file: UploadFile = File(...)):   
    content = await file.read()
    image_base64 = base64.b64encode(content).decode("utf-8") #codifica la imagen en base64(pasa la imagen a string)

    upload_file = imagekit.upload( 
        file = image_base64, #se especifica el archivo a subir
        file_name=str(datetime.now()), #se especifica el nombre del archivo
        options=UploadFileRequestOptions( #se especifican las opciones de subida(con las que hay ahora tenemos suficiente)
            use_unique_file_name=False,
            folder=foldername
        )
    )
    
    #create_folder = imagekit.create_folder(options=CreateFolderRequestOptions(folder_name="test", parent_folder_path="/"))
    #print("Create folder-", create_folder, end="\n\n")

    # Raw Response
    return upload_file.response_metadata.raw