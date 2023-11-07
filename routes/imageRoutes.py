from fastapi import FastAPI, HTTPException, Depends, APIRouter
from typing import List, Annotated
from sqlalchemy.orm import Session
from database import SessionLocal, engine, UserBase, RouteBase

from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 
db_dependency = Annotated[Session, Depends(get_db)]

extensions = [
    {
        'name': 'remove-bg',
        'options': {
            'add_shadow': True,
            'bg_color': 'pink'
        }
    },
    {
        'name': 'google-auto-tagging',
        'minConfidence': 80,
        'maxTags': 10
    }
]

options = UploadFileRequestOptions(
    use_unique_file_name=False,
    tags=['abc', 'def'],
    folder='/testing-python-folder/',
    is_private_file=False,
    custom_coordinates='10,10,20,20',
    response_fields=['tags', 'custom_coordinates', 'is_private_file',
                     'embedded_metadata', 'custom_metadata'],
    extensions=extensions,
    webhook_url='https://webhook.site/c78d617f-33bc-40d9-9e61-608999721e2e',
    overwrite_file=True,
    overwrite_ai_tags=False,
    overwrite_tags=False,
    overwrite_custom_metadata=True,
    custom_metadata={'testss': 12},
)

result = imagekit.upload_file(file='<url|base_64|binary>', # required
                              file_name='my_file_name.jpg', # required
                              options=options)

# Final Result
print(result)

# Raw Response
print(result.response_metadata.raw)

# print that uploaded file's ID
print(result.file_id)