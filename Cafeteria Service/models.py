from pydantic import BaseModel
from typing import Optional

# Main Menu Item Model
class MenuItem(BaseModel):
    id: str
    name: str
    category: str
    price: float
    available: bool
    meal_time: str

# Required details when creating a new menu item
class MenuItemCreate(BaseModel):
    name: str
    category: str
    price: float
    available: bool
    meal_time: str

# Required details when updating a menu item
class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None
    meal_time: Optional[str] = None