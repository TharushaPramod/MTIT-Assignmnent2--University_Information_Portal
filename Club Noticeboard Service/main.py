from fastapi import FastAPI, HTTPException, status
from models import Notice, NoticeCreate, NoticeUpdate
from service import NoticeService
from typing import List

app = FastAPI(title="Club Noticeboard Microservice", version="1.0.0")

notice_service = NoticeService()

@app.get("/")
def read_root():
    return {"message": "Club Noticeboard Service is running perfectly with MongoDB!"}

@app.get("/api/notices", response_model=List[Notice])
def get_all_notices():
    """Get all club notices"""
    return notice_service.get_all()

@app.get("/api/notices/{notice_id}", response_model=Notice)
def get_notice(notice_id: str):
    """Get a notice by ID"""
    notice = notice_service.get_by_id(notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@app.post("/api/notices", response_model=Notice, status_code=status.HTTP_201_CREATED)
def create_notice(notice: NoticeCreate):
    """Publish a new notice"""
    return notice_service.create(notice)

@app.put("/api/notices/{notice_id}", response_model=Notice)
def update_notice(notice_id: str, notice: NoticeUpdate):
    """Update an existing notice"""
    updated_notice = notice_service.update(notice_id, notice)
    if not updated_notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return updated_notice

@app.delete("/api/notices/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notice(notice_id: str):
    """Delete a notice"""
    success = notice_service.delete(notice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notice not found")
    return None