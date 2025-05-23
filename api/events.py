from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from db import models
from api.models import schemas
from db.database import get_db

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

# Event operations
def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def get_events_by_period(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    """Get events within a specific time period (war period)"""
    query = db.query(models.Event)
    
    # Apply date filters if provided
    # Note: This is a placeholder. In a real application, you would need to 
    # add date fields to the Event model to properly filter by period
    
    return query.all()

# Removed add_veteran_to_event function as relationships should be created by neural network analysis

# API endpoints
@router.get("/war-period", response_model=List[schemas.EventLocation])
def get_events_by_war_period(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """
    Get events by war period, returning only location data (lat, long, name, description)
    """
    # Convert string dates to datetime if provided
    start_datetime = None
    end_datetime = None
    
    if start_date:
        try:
            start_datetime = datetime.fromisoformat(start_date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid start_date format. Use ISO format (YYYY-MM-DD)."
            )
    
    if end_date:
        try:
            end_datetime = datetime.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid end_date format. Use ISO format (YYYY-MM-DD)."
            )
    
    events = get_events_by_period(db, start_datetime, end_datetime)
    
    # Return only the required fields
    return [
        schemas.EventLocation(
            name=event.name,
            description=event.description,
            latitude=event.latitude,
            longitude=event.longitude
        ) for event in events
    ]

@router.get("/{event_id}/veterans-graph", response_model=schemas.EventVeteransGraph)
def get_event_veterans_graph(event_id: int, db: Session = Depends(get_db)):
    """
    Get veterans related to an event and their connections for graph visualization
    """
    db_event = get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Get all veterans related to this event
    veterans = db_event.veterans
    
    # Create nodes for each veteran
    nodes = [
        schemas.VeteranNode(id=veteran.id, name=veteran.name)
        for veteran in veterans
    ]
    
    # Create connections between veterans
    connections = []
    for veteran in veterans:
        for related_veteran in veteran.related_veterans:
            # Only include connections between veterans that are part of this event
            if related_veteran in veterans:
                connections.append(
                    schemas.VeteranConnection(
                        source=veteran.id,
                        target=related_veteran.id
                    )
                )
    
    return schemas.EventVeteransGraph(nodes=nodes, connections=connections)

# Removed add_veteran_to_event_endpoint as relationships should be created by neural network analysis
