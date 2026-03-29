from fastapi import FastAPI, HTTPException, status
from models import Event, EventCreate, EventUpdate
from service import EventService
from typing import List

app = FastAPI(title="Event Management Service", version="1.0.0")

# Initialize service
event_service = EventService()

@app.get("/")
def read_root():
    return {"message": "Event Management Service is running"}

@app.get("/api/events", response_model=List[Event])
def get_all_events():
    """Get all events"""
    return event_service.get_all()

@app.get("/api/events/{event_id}", response_model=Event)
def get_event(event_id: int):
    """Get an event by ID"""
    event = event_service.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/api/events", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate):
    """Create a new event"""
    return event_service.create(event)

@app.put("/api/events/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventUpdate):
    """Update an event"""
    updated_event = event_service.update(event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event

@app.delete("/api/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int):
    """Delete an event"""
    success = event_service.delete(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return None
