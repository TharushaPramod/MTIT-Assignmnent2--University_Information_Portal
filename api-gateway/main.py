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
    "directory": "http://localhost:8001",
    "cafeteria": "http://localhost:8002",
    "noticeboard": "http://localhost:8003",
    "lostfound": "http://localhost:8004",
    "events": "http://localhost:8005",
    "shuttle": "http://localhost:8006"
}

# ==========================================
# 2. PYDANTIC MODELS
# ==========================================
# --- Directory Models ---
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

# --- Cafeteria Models ---
class MenuItemCreate(BaseModel):
    name: str
    category: str
    price: float
    available: bool
    meal_time: str

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None
    meal_time: Optional[str] = None

# --- Noticeboard Models ---
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

# --- Lost & Found Models ---
class LostFoundItemCreate(BaseModel):
    itemName: str
    description: str
    category: str
    location: str
    reportedBy: str
    contactInfo: str
    type: str

class LostFoundItemUpdate(BaseModel):
    itemName: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    reportedBy: Optional[str] = None
    contactInfo: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None

class LostFoundStatusUpdate(BaseModel):
    status: str

# --- Event Management Models ---
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

# --- Shuttle Service Models ---
class ShuttleRouteCreate(BaseModel):
    routeName: str
    startLocation: str
    endLocation: str
    stops: str
    distanceKm: str
    isActive: bool = True

class ShuttleRouteUpdate(BaseModel):
    routeName: Optional[str] = None
    startLocation: Optional[str] = None
    endLocation: Optional[str] = None
    stops: Optional[str] = None
    distanceKm: Optional[str] = None
    isActive: Optional[bool] = None

class ShuttleScheduleCreate(BaseModel):
    routeName: str
    departureTime: str
    arrivalTime: str
    daysOfWeek: str
    busNumber: str
    driverName: str
    totalSeats: int = 40
    availableSeats: int = 40
    isActive: bool = True

class ShuttleScheduleUpdate(BaseModel):
    routeName: Optional[str] = None
    departureTime: Optional[str] = None
    arrivalTime: Optional[str] = None
    daysOfWeek: Optional[str] = None
    busNumber: Optional[str] = None
    driverName: Optional[str] = None
    totalSeats: Optional[int] = None
    availableSeats: Optional[int] = None
    isActive: Optional[bool] = None

class ShuttleSeatsUpdate(BaseModel):
    availableSeats: int

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
            elif method == "PATCH":
                response = await client.patch(url, **kwargs)
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

@app.get("/", tags=["System"])
def read_root():
    return {"message": "API Gateway is running. Welcome to University Portal!"}

# ==========================================
# 4. DIRECTORY SERVICE ROUTES (Port 8001)
# ==========================================
@app.get("/gateway/directory", tags=["Directory"], operation_id="GetAllStaff")
async def get_all_staff():
    return await forward_request("directory", "/api/staff", "GET")

@app.get("/gateway/directory/{staff_id}", tags=["Directory"], operation_id="GetStaffById")
async def get_staff_member(staff_id: str):
    return await forward_request("directory", f"/api/staff/{staff_id}", "GET")

@app.post("/gateway/directory", tags=["Directory"], operation_id="CreateStaff")
async def create_staff_member(body: StaffMemberCreate):
    return await forward_request("directory", "/api/staff", "POST", json=body.dict())

@app.put("/gateway/directory/{staff_id}", tags=["Directory"], operation_id="UpdateStaff")
async def update_staff_member(staff_id: str, body: StaffMemberUpdate):
    return await forward_request("directory", f"/api/staff/{staff_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/directory/{staff_id}", tags=["Directory"], operation_id="DeleteStaff")
async def delete_staff_member(staff_id: str):
    return await forward_request("directory", f"/api/staff/{staff_id}", "DELETE")

# ==========================================
# 5. CAFETERIA SERVICE ROUTES (Port 8002)
# ==========================================
@app.get("/gateway/cafeteria", tags=["Cafeteria"], operation_id="GetAllMenu")
async def get_all_menu_items():
    return await forward_request("cafeteria", "/api/menu", "GET")

@app.get("/gateway/cafeteria/{item_id}", tags=["Cafeteria"], operation_id="GetMenuById")
async def get_menu_item(item_id: str):
    return await forward_request("cafeteria", f"/api/menu/{item_id}", "GET")

@app.post("/gateway/cafeteria", tags=["Cafeteria"], operation_id="CreateMenu")
async def create_menu_item(body: MenuItemCreate):
    return await forward_request("cafeteria", "/api/menu", "POST", json=body.dict())

@app.put("/gateway/cafeteria/{item_id}", tags=["Cafeteria"], operation_id="UpdateMenu")
async def update_menu_item(item_id: str, body: MenuItemUpdate):
    return await forward_request("cafeteria", f"/api/menu/{item_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/cafeteria/{item_id}", tags=["Cafeteria"], operation_id="DeleteMenu")
async def delete_menu_item(item_id: str):
    return await forward_request("cafeteria", f"/api/menu/{item_id}", "DELETE")

# ==========================================
# 6. CLUB NOTICEBOARD ROUTES (Port 8003)
# ==========================================
@app.get("/gateway/notices", tags=["Noticeboard"], operation_id="GetAllNotices")
async def get_all_notices():
    return await forward_request("noticeboard", "/api/notices", "GET")

@app.get("/gateway/notices/{notice_id}", tags=["Noticeboard"], operation_id="GetNoticeById")
async def get_notice(notice_id: str):
    return await forward_request("noticeboard", f"/api/notices/{notice_id}", "GET")

@app.post("/gateway/notices", tags=["Noticeboard"], operation_id="CreateNotice")
async def create_notice(body: NoticeCreate):
    return await forward_request("noticeboard", "/api/notices", "POST", json=body.dict())

@app.put("/gateway/notices/{notice_id}", tags=["Noticeboard"], operation_id="UpdateNotice")
async def update_notice(notice_id: str, body: NoticeUpdate):
    return await forward_request("noticeboard", f"/api/notices/{notice_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/notices/{notice_id}", tags=["Noticeboard"], operation_id="DeleteNotice")
async def delete_notice(notice_id: str):
    return await forward_request("noticeboard", f"/api/notices/{notice_id}", "DELETE")

# ==========================================
# 7. LOST & FOUND SERVICE ROUTES (Port 8004)
# ==========================================
@app.get("/gateway/lost-found", tags=["Lost & Found"], operation_id="GetAllLFItems")
async def get_all_items():
    return await forward_request("lostfound", "/items", "GET")

@app.get("/gateway/lost-found/lost", tags=["Lost & Found"], operation_id="GetLostItems")
async def get_lost_items():
    return await forward_request("lostfound", "/items/lost", "GET")

@app.get("/gateway/lost-found/found", tags=["Lost & Found"], operation_id="GetFoundItems")
async def get_found_items():
    return await forward_request("lostfound", "/items/found", "GET")

@app.get("/gateway/lost-found/{item_id}", tags=["Lost & Found"], operation_id="GetLFItemById")
async def get_lf_item(item_id: str):
    return await forward_request("lostfound", f"/items/{item_id}", "GET")

@app.post("/gateway/lost-found", tags=["Lost & Found"], operation_id="CreateLFItem")
async def create_lf_item(body: LostFoundItemCreate):
    return await forward_request("lostfound", "/items", "POST", json=body.dict())

@app.put("/gateway/lost-found/{item_id}", tags=["Lost & Found"], operation_id="UpdateLFItem")
async def update_lf_item(item_id: str, body: LostFoundItemUpdate):
    return await forward_request("lostfound", f"/items/{item_id}", "PUT", json=body.dict(exclude_unset=True))

@app.patch("/gateway/lost-found/{item_id}/status", tags=["Lost & Found"], operation_id="UpdateLFStatus")
async def update_lf_status(item_id: str, body: LostFoundStatusUpdate):
    return await forward_request("lostfound", f"/items/{item_id}/status", "PATCH", json=body.dict())

@app.delete("/gateway/lost-found/{item_id}", tags=["Lost & Found"], operation_id="DeleteLFItem")
async def delete_lf_item(item_id: str):
    return await forward_request("lostfound", f"/items/{item_id}", "DELETE")

# ==========================================
# 8. EVENT MANAGEMENT ROUTES (Port 8005)
# ==========================================
@app.get("/gateway/events", tags=["Events"], operation_id="GetAllEvents")
async def get_all_events():
    return await forward_request("events", "/api/events", "GET")

@app.post("/gateway/events", tags=["Events"], operation_id="CreateEvent")
async def create_event(body: EventCreate):
    return await forward_request("events", "/api/events", "POST", json=body.dict())

@app.put("/gateway/events/{event_id}", tags=["Events"], operation_id="UpdateEvent")
async def update_event(event_id: str, body: EventUpdate):
    return await forward_request("events", f"/api/events/{event_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/events/{event_id}", tags=["Events"], operation_id="DeleteEvent")
async def delete_event(event_id: str):
    return await forward_request("events", f"/api/events/{event_id}", "DELETE")

# ==========================================
# 9. SHUTTLE SERVICE ROUTES (Port 8006)
# ==========================================
@app.post("/gateway/shuttle/routes", tags=["Shuttle Service"], operation_id="CreateRoute")
async def create_route(body: ShuttleRouteCreate):
    return await forward_request("shuttle", "/routes", "POST", json=body.dict())

@app.get("/gateway/shuttle/routes", tags=["Shuttle Service"], operation_id="GetAllRoutes")
async def get_routes():
    return await forward_request("shuttle", "/routes", "GET")

@app.put("/gateway/shuttle/routes/{route_id}", tags=["Shuttle Service"], operation_id="UpdateRoute")
async def update_route(route_id: str, body: ShuttleRouteUpdate):
    return await forward_request("shuttle", f"/routes/{route_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/shuttle/routes/{route_id}", tags=["Shuttle Service"], operation_id="DeleteRoute")
async def delete_route(route_id: str):
    return await forward_request("shuttle", f"/routes/{route_id}", "DELETE")

@app.post("/gateway/shuttle/schedules", tags=["Shuttle Service"], operation_id="CreateSchedule")
async def create_schedule(body: ShuttleScheduleCreate):
    return await forward_request("shuttle", "/schedules", "POST", json=body.dict())

@app.get("/gateway/shuttle/schedules", tags=["Shuttle Service"], operation_id="GetAllSchedules")
async def get_schedules():
    return await forward_request("shuttle", "/schedules", "GET")

@app.put("/gateway/shuttle/schedules/{schedule_id}", tags=["Shuttle Service"], operation_id="UpdateSchedule")
async def update_schedule(schedule_id: str, body: ShuttleScheduleUpdate):
    return await forward_request("shuttle", f"/schedules/{schedule_id}", "PUT", json=body.dict(exclude_unset=True))

@app.patch("/gateway/shuttle/schedules/{schedule_id}/seats", tags=["Shuttle Service"], operation_id="UpdateSeats")
async def update_available_seats(schedule_id: str, body: ShuttleSeatsUpdate):
    return await forward_request("shuttle", f"/schedules/{schedule_id}/seats", "PATCH", json=body.dict())

@app.delete("/gateway/shuttle/schedules/{schedule_id}", tags=["Shuttle Service"], operation_id="DeleteSchedule")
async def delete_schedule(schedule_id: str):
    return await forward_request("shuttle", f"/schedules/{schedule_id}", "DELETE")