from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    id: int
    title: str
    description: str
    date: str
    time: str
    venue: str
    event_type: str

class EventCreate(BaseModel):
    title: str
    description: str
    date: str
    time: str
    venue: str
    event_type: str

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    venue: Optional[str] = None
    event_type: Optional[str] = None
