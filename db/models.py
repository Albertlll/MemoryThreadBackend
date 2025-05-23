from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.database import Base

# Association table for many-to-many relationship between Veterans and Events
veteran_event = Table(
    "veteran_event",
    Base.metadata,
    Column("veteran_id", Integer, ForeignKey("veterans.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True)
)

# Association table for many-to-many relationship between Veterans
veteran_relationship = Table(
    "veteran_relationship",
    Base.metadata,
    Column("veteran_id", Integer, ForeignKey("veterans.id"), primary_key=True),
    Column("related_veteran_id", Integer, ForeignKey("veterans.id"), primary_key=True)
)

class Veteran(Base):
    __tablename__ = "veterans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    biography = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    death_date = Column(DateTime, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    events = relationship(
        "Event",
        secondary=veteran_event,
        back_populates="veterans"
    )
    
    # Self-referential relationship for veterans who served together
    related_veterans = relationship(
        "Veteran",
        secondary=veteran_relationship,
        primaryjoin=(veteran_relationship.c.veteran_id == id),
        secondaryjoin=(veteran_relationship.c.related_veteran_id == id),
        backref="related_to"
    )

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    historical_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    veterans = relationship(
        "Veteran",
        secondary=veteran_event,
        back_populates="events"
    )
