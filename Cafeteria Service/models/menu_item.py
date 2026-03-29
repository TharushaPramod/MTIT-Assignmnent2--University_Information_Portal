from beanie import Document
from typing import Optional
from enum import Enum

class Category(str, Enum):
    rice = "Rice"
    short_eats = "Short Eats"
    beverages = "Beverages"
    desserts = "Desserts"

class MenuItem(Document):
    name: str
    price: float
    category: Category
    available: bool = True
    description: Optional[str] = None

    class Settings:
        name = "menuitems"  # MongoDB collection name