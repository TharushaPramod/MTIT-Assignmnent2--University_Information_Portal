from fastapi import FastAPI, HTTPException
from schemas import Route, UpdateRouteModel, ShuttleSchedule, UpdateScheduleModel, UpdateSeatsModel
from model import *

app = FastAPI(title="Shuttle Bus Service")


@app.get("/")
def home():
    return {"message": "Shuttle Bus Service is running"}


# ═══════════════════════════════════════════
#  ROUTE ENDPOINTS
# ═══════════════════════════════════════════

# CREATE ROUTE
@app.post("/routes")
def add_route(route: Route):
    new_route = create_route(route.dict())
    return route_serializer(new_route)

# GET ALL ROUTES
@app.get("/routes")
def get_routes():
    return get_all_routes()

# GET ACTIVE ROUTES ONLY
@app.get("/routes/active")
def get_routes_active():
    return get_active_routes()

# GET ROUTE BY ID
@app.get("/routes/{route_id}")
def get_route(route_id: str):
    route = get_route_by_id(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route_serializer(route)

# UPDATE ROUTE
@app.put("/routes/{route_id}")
def update_route_endpoint(route_id: str, data: UpdateRouteModel):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    route = update_route(route_id, update_data)
    return route_serializer(route)

# DELETE ROUTE
@app.delete("/routes/{route_id}")
def delete_route_endpoint(route_id: str):
    delete_route(route_id)
    return {"message": "Route deleted successfully"}


# ═══════════════════════════════════════════
#  SCHEDULE ENDPOINTS
# ═══════════════════════════════════════════

# CREATE SCHEDULE
@app.post("/schedules")
def add_schedule(schedule: ShuttleSchedule):
    new_schedule = create_schedule(schedule.dict())
    return schedule_serializer(new_schedule)

# GET ALL SCHEDULES
@app.get("/schedules")
def get_schedules():
    return get_all_schedules()

# GET SCHEDULES BY ROUTE NAME
@app.get("/schedules/route/{route_name}")
def get_by_route(route_name: str):
    return get_schedules_by_route(route_name)

# GET ACTIVE SCHEDULES ONLY
@app.get("/schedules/active")
def get_schedules_active():
    return get_active_schedules()

# GET SCHEDULE BY ID
@app.get("/schedules/{schedule_id}")
def get_schedule(schedule_id: str):
    schedule = get_schedule_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule_serializer(schedule)

# UPDATE SCHEDULE
@app.put("/schedules/{schedule_id}")
def update_schedule_endpoint(schedule_id: str, data: UpdateScheduleModel):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    schedule = update_schedule(schedule_id, update_data)
    return schedule_serializer(schedule)

# UPDATE AVAILABLE SEATS
@app.patch("/schedules/{schedule_id}/seats")
def update_available_seats(schedule_id: str, seats_data: UpdateSeatsModel):
    schedule = update_seats(schedule_id, seats_data.availableSeats)
    return schedule_serializer(schedule)

# DELETE SCHEDULE
@app.delete("/schedules/{schedule_id}")
def delete_schedule_endpoint(schedule_id: str):
    delete_schedule(schedule_id)
    return {"message": "Schedule deleted successfully"}
