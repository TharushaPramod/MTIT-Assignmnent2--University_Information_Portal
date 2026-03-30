from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI(title="University Portal API Gateway", version="1.0.0")

# ==========================================
# 1. MICROSERVICES URL REGISTRY
# ==========================================
SERVICES = {
    "noticeboard": "http://localhost:8006",
   
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

