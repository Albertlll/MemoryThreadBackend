from pydantic import BaseModel
from typing import List, Optional, Dict, Literal
from datetime import datetime

# Event schemas
class EventBase(BaseModel):
    name: str
    historical_name: Optional[str] = None
    description: Optional[str] = None
    latitude: float
    longitude: float
    image_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime
    veterans: List["Veteran"] = []

    class Config:
        from_attributes = True

# Simplified Event schema for war period endpoint
class EventLocation(BaseModel):
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

# Veteran schemas
class VeteranBase(BaseModel):
    name: str
    biography: Optional[str] = None
    history: Optional[str] = None  # Detailed history like a Wikipedia article
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    image_url: Optional[str] = None

class VeteranCreate(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    biography: str
    image_base64: str

class Veteran(VeteranBase):
    id: int
    created_at: datetime
    events: List[Event] = []
    related_veterans: List["Veteran"] = []

    class Config:
        from_attributes = True

# Simplified Veteran schema for specific veteran info
class VeteranInfo(BaseModel):
    id: int
    name: str
    biography: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

# Schema for veterans graph data
class VeteranNode(BaseModel):
    id: int
    name: str

class VeteranConnection(BaseModel):
    source: int  # veteran_id
    target: int  # related_veteran_id

class EventVeteransGraph(BaseModel):
    nodes: List[VeteranNode]
    connections: List[VeteranConnection]

# Response message schemas
class ResponseStatus(BaseModel):
    status: Literal["success", "error", "warning"]
    message: str
    data: Optional[dict] = None

# Update forward references
Veteran.model_rebuild()
