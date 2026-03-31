from database import shuttle_collection, route_collection
from bson import ObjectId


# ── Serializers ────────────────────────────────────────────────

def route_serializer(route) -> dict:
    return {
        "id": str(route["_id"]),
        "routeName": route["routeName"],
        "startLocation": route["startLocation"],
        "endLocation": route["endLocation"],
        "stops": route["stops"],
        "distanceKm": route["distanceKm"],
        "isActive": route["isActive"],
    }


def schedule_serializer(schedule) -> dict:
    return {
        "id": str(schedule["_id"]),
        "routeName": schedule["routeName"],
        "departureTime": schedule["departureTime"],
        "arrivalTime": schedule["arrivalTime"],
        "daysOfWeek": schedule["daysOfWeek"],
        "busNumber": schedule["busNumber"],
        "driverName": schedule["driverName"],
        "totalSeats": schedule["totalSeats"],
        "availableSeats": schedule["availableSeats"],
        "isActive": schedule["isActive"],
    }


# ── Route CRUD ─────────────────────────────────────────────────

def create_route(data: dict):
    result = route_collection.insert_one(data)
    return route_collection.find_one({"_id": result.inserted_id})

def get_all_routes():
    return [route_serializer(r) for r in route_collection.find()]

def get_active_routes():
    return [route_serializer(r) for r in route_collection.find({"isActive": True})]

def get_route_by_id(route_id: str):
    return route_collection.find_one({"_id": ObjectId(route_id)})

def update_route(route_id: str, data: dict):
    route_collection.update_one({"_id": ObjectId(route_id)}, {"$set": data})
    return route_collection.find_one({"_id": ObjectId(route_id)})

def delete_route(route_id: str):
    return route_collection.delete_one({"_id": ObjectId(route_id)})


# ── Schedule CRUD ──────────────────────────────────────────────

def create_schedule(data: dict):
    result = shuttle_collection.insert_one(data)
    return shuttle_collection.find_one({"_id": result.inserted_id})

def get_all_schedules():
    return [schedule_serializer(s) for s in shuttle_collection.find()]

def get_schedules_by_route(route_name: str):
    return [schedule_serializer(s) for s in shuttle_collection.find({"routeName": route_name})]

def get_active_schedules():
    return [schedule_serializer(s) for s in shuttle_collection.find({"isActive": True})]

def get_schedule_by_id(schedule_id: str):
    return shuttle_collection.find_one({"_id": ObjectId(schedule_id)})

def update_schedule(schedule_id: str, data: dict):
    shuttle_collection.update_one({"_id": ObjectId(schedule_id)}, {"$set": data})
    return shuttle_collection.find_one({"_id": ObjectId(schedule_id)})

def update_seats(schedule_id: str, available_seats: int):
    shuttle_collection.update_one(
        {"_id": ObjectId(schedule_id)},
        {"$set": {"availableSeats": available_seats}}
    )
    return shuttle_collection.find_one({"_id": ObjectId(schedule_id)})

def delete_schedule(schedule_id: str):
    return shuttle_collection.delete_one({"_id": ObjectId(schedule_id)})
