from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI(title="University Portal API Gateway", version="1.0.0")

# ==========================================
# 1. MICROSERVICES URL REGISTRY
# ==========================================
# Noticeboard eka 8006 wala, Events eka 8001 wala run wenawa kiyala hithamu
SERVICES = {
    "noticeboard": "http://localhost:8006",
    "events": "http://localhost:8001"  
}

# ==========================================
# 2. PYDANTIC MODELS (Swagger Text Boxes Walata)
# ==========================================
# Noticeboard Models
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

# Event Management Models (Yaluwage eken gaththa)
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

# ==========================================
# 3. MAIN GATEWAY FORWARDING LOGIC
# ==========================================
async def forward_request(service: str, path: str, method: str, **kwargs):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")
    
    url = f"{SERVICES[service]}{path}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "API Gateway is running. Welcome to University Portal!"}

# ==========================================
# 4. CLUB NOTICEBOARD ROUTES (Port 8006)
# ==========================================
@app.get("/gateway/notices")
async def get_all_notices():
    return await forward_request("noticeboard", "/api/notices", "GET")

@app.get("/gateway/notices/{notice_id}")
async def get_notice(notice_id: str):
    return await forward_request("noticeboard", f"/api/notices/{notice_id}", "GET")

@app.post("/gateway/notices")
async def create_notice(body: NoticeCreate):
    return await forward_request("noticeboard", "/api/notices", "POST", json=body.dict())

@app.put("/gateway/notices/{notice_id}")
async def update_notice(notice_id: str, body: NoticeUpdate):
    return await forward_request("noticeboard", f"/api/notices/{notice_id}", "PUT", json=body.dict())

@app.delete("/gateway/notices/{notice_id}")
async def delete_notice(notice_id: str):
    return await forward_request("noticeboard", f"/api/notices/{notice_id}", "DELETE")

# ==========================================
# 5. EVENT MANAGEMENT ROUTES (Port 8001)
# ==========================================
@app.get("/gateway/events")
async def get_all_events():
    # Yaluwage route eka thibbe /api/events kiyala nisa eka denawa
    return await forward_request("events", "/api/events", "GET")

@app.get("/gateway/events/{event_id}")
async def get_event(event_id: str):
    return await forward_request("events", f"/api/events/{event_id}", "GET")

@app.post("/gateway/events")
async def create_event(body: EventCreate):
    return await forward_request("events", "/api/events", "POST", json=body.dict())

@app.put("/gateway/events/{event_id}")
async def update_event(event_id: str, body: EventUpdate):
    return await forward_request("events", f"/api/events/{event_id}", "PUT", json=body.dict())

@app.delete("/gateway/events/{event_id}")
async def delete_event(event_id: str):
    return await forward_request("events", f"/api/events/{event_id}", "DELETE")