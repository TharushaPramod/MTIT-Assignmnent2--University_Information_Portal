from pydantic import BaseModel
from typing import Optional

# Pradhana Notice Model eka
class Notice(BaseModel):
    id: str
    club_name: str
    title: str
    content: str
    date: str

# Aluth notice ekak daddi awashya wena details
class NoticeCreate(BaseModel):
    club_name: str
    title: str
    content: str
    date: str

# Notice ekak update karaddi awashya wena details
class NoticeUpdate(BaseModel):
    club_name: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    date: Optional[str] = None