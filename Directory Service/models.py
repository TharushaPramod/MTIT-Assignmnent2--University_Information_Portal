from pydantic import BaseModel
from typing import Optional

class StaffMember(BaseModel):
    id: str
    name: str
    designation: str          # e.g., "Senior Lecturer", "Administrative Officer"
    department: str           # e.g., "Faculty of IT", "Registrar's Office"
    email: str
    phone: str
    room_number: str          # e.g., "IT-203", "Admin Block Room 5"
    office_hours: str         # e.g., "Mon/Wed 9:00 AM - 11:00 AM"

class StaffMemberCreate(BaseModel):
    name: str
    designation: str
    department: str
    email: str
    phone: str
    room_number: str
    office_hours: str

class StaffMemberUpdate(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    room_number: Optional[str] = None
    office_hours: Optional[str] = None
