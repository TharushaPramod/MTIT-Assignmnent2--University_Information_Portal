from fastapi import FastAPI, HTTPException, status
from models import StaffMember, StaffMemberCreate, StaffMemberUpdate
from service import StaffService
from typing import List

app = FastAPI(title="Directory Service Microservice", version="1.0.0")

staff_service = StaffService()

@app.get("/")
def read_root():
    return {"message": "Directory Service is running perfectly with MongoDB!"}

@app.get("/api/staff", response_model=List[StaffMember])
def get_all_staff():
    """Get all staff members (lecturers & admin)"""
    return staff_service.get_all()

@app.get("/api/staff/{staff_id}", response_model=StaffMember)
def get_staff_member(staff_id: str):
    """Get a staff member by ID"""
    member = staff_service.get_by_id(staff_id)
    if not member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return member

@app.post("/api/staff", response_model=StaffMember, status_code=status.HTTP_201_CREATED)
def create_staff_member(member: StaffMemberCreate):
    """Add a new staff member to the directory"""
    return staff_service.create(member)

@app.put("/api/staff/{staff_id}", response_model=StaffMember)
def update_staff_member(staff_id: str, member: StaffMemberUpdate):
    """Update an existing staff member's details"""
    updated_member = staff_service.update(staff_id, member)
    if not updated_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return updated_member

@app.delete("/api/staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff_member(staff_id: str):
    """Remove a staff member from the directory"""
    success = staff_service.delete(staff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return None
