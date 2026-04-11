from pydantic import BaseModel
from typing import Optional


# ── Route Schemas ──────────────────────────────────────────────

class Route(BaseModel):
    routeName: str
    startLocation: str
    endLocation: str
    stops: str          # Comma-separated intermediate stops
    distanceKm: str
    isActive: bool = True


class UpdateRouteModel(BaseModel):
    routeName: Optional[str] = None
    startLocation: Optional[str] = None
    endLocation: Optional[str] = None
    stops: Optional[str] = None
    distanceKm: Optional[str] = None
    isActive: Optional[bool] = None


# ── Schedule Schemas ───────────────────────────────────────────

class ShuttleSchedule(BaseModel):
    routeName: str          # Reference to route by name
    departureTime: str      # e.g. "07:30"
    arrivalTime: str        # e.g. "08:15"
    daysOfWeek: str         # e.g. "Mon,Tue,Wed,Thu,Fri"
    busNumber: str          # e.g. "NB-1234"
    driverName: str
    totalSeats: int = 40
    availableSeats: int = 40
    isActive: bool = True


class UpdateScheduleModel(BaseModel):
    routeName: Optional[str] = None
    departureTime: Optional[str] = None
    arrivalTime: Optional[str] = None
    daysOfWeek: Optional[str] = None
    busNumber: Optional[str] = None
    driverName: Optional[str] = None
    totalSeats: Optional[int] = None
    availableSeats: Optional[int] = None
    isActive: Optional[bool] = None


class UpdateSeatsModel(BaseModel):
    availableSeats: int
