from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from typing import Any

app = FastAPI(title="API Gateway", version="1.0.0")

# Service URLs
SERVICES = {
    "event": "http://localhost:8001"
}

async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice"""
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
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}

# Event Service Routes
@app.get("/gateway/events")
async def get_all_events():
    """Get all events through gateway"""
    return await forward_request("event", "/api/events", "GET")

@app.get("/gateway/events/{event_id}")
async def get_event(event_id: int):
    """Get an event by ID through gateway"""
    return await forward_request("event", f"/api/events/{event_id}", "GET")

@app.post("/gateway/events")
async def create_event(request: Request):
    """Create a new event through gateway"""
    body = await request.json()
    return await forward_request("event", "/api/events", "POST", json=body)

@app.put("/gateway/events/{event_id}")
async def update_event(event_id: int, request: Request):
    """Update an event through gateway"""
    body = await request.json()
    return await forward_request("event", f"/api/events/{event_id}", "PUT", json=body)

@app.delete("/gateway/events/{event_id}")
async def delete_event(event_id: int):
    """Delete an event through gateway"""
    return await forward_request("event", f"/api/events/{event_id}", "DELETE")
