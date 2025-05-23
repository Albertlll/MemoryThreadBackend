from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import base64
import os
from datetime import datetime

from db import models
from api.models import schemas
from db.database import get_db

router = APIRouter(
    prefix="/veterans",
    tags=["veterans"],
    responses={404: {"description": "Not found"}},
)

# Veteran operations
def get_veteran(db: Session, veteran_id: int):
    return db.query(models.Veteran).filter(models.Veteran.id == veteran_id).first()

def create_veteran_with_image(db: Session, veteran_data: schemas.VeteranCreate):
    """Create a new veteran with image data in base64 format"""
    # Construct the full name
    full_name = f"{veteran_data.last_name} {veteran_data.first_name}"
    if veteran_data.patronymic:
        full_name += f" {veteran_data.patronymic}"
    
    # Process the base64 image
    # In a real application, you would save this to a file or cloud storage
    # and store the URL in the database
    image_url = None
    if veteran_data.image_base64:
        # For this example, we'll assume the image is stored and we have a URL
        # In a real app, you would decode the base64 and save the image
        image_url = f"images/veteran_{datetime.now().timestamp()}.jpg"
    
    # Create the veteran record
    db_veteran = models.Veteran(
        name=full_name,
        biography=veteran_data.biography,
        image_url=image_url
    )
    
    db.add(db_veteran)
    db.commit()
    db.refresh(db_veteran)
    return db_veteran

# Removed add_related_veteran function as relationships should be created by neural network analysis

# API endpoints
@router.post("/", response_model=schemas.ResponseStatus, status_code=status.HTTP_201_CREATED)
def submit_veteran_info(veteran: schemas.VeteranCreate, db: Session = Depends(get_db)):
    """
    Submit information about a veteran including biography and image
    Returns a status message indicating success or failure
    """
    try:
        db_veteran = create_veteran_with_image(db=db, veteran_data=veteran)
        
        # Return success response with veteran ID in the data
        return schemas.ResponseStatus(
            status="success",
            message="Veteran information submitted successfully",
            data={"veteran_id": db_veteran.id}
        )
    except Exception as e:
        # Return error response
        return schemas.ResponseStatus(
            status="error",
            message=f"Failed to submit veteran information: {str(e)}"
        )

@router.get("/{veteran_id}", response_model=schemas.VeteranInfo)
def get_veteran_info(veteran_id: int, db: Session = Depends(get_db)):
    """
    Get information about a specific veteran (image and text)
    """
    db_veteran = get_veteran(db, veteran_id=veteran_id)
    if db_veteran is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veteran not found"
        )
    
    return schemas.VeteranInfo(
        id=db_veteran.id,
        name=db_veteran.name,
        biography=db_veteran.biography,
        image_url=db_veteran.image_url
    )

# Removed add_related_veteran_endpoint as relationships should be created by neural network analysis
