from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LostFoundItem(BaseModel):
    itemName: str
    description: str
    category: str
    location: str
    reportedBy: str
    contactInfo: str
    type: str  # lost or found
    status: str = "lost"  # lost, found, claimed, returned
    dateReported: datetime = Field(default_factory=datetime.utcnow)

class UpdateStatusModel(BaseModel):
    status: str

class UpdateItemModel(BaseModel):
    itemName: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    reportedBy: Optional[str] = None
    contactInfo: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None