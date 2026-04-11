from pydantic import BaseModel
from typing import Optional

class Notice(BaseModel):
    id: str
    club_name: str
    title: str
    content: str
    date: str

class NoticeCreate(BaseModel):
    club_name: str
    title: str
    content: str
    date: str

class NoticeUpdate(BaseModel):
    club_name: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    date: Optional[str] = None