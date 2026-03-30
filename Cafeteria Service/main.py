from fastapi import FastAPI, HTTPException, status
from models import MenuItem, MenuItemCreate, MenuItemUpdate
from service import CafeteriaService
from typing import List

app = FastAPI(title="Cafeteria Microservice", version="1.0.0")

cafeteria_service = CafeteriaService()

@app.get("/")
def read_root():
    return {"message": "Cafeteria Service is running perfectly with MongoDB!"}

@app.get("/api/menu", response_model=List[MenuItem])
def get_all_menu_items():
    """Get all menu items"""
    return cafeteria_service.get_all()

@app.get("/api/menu/{item_id}", response_model=MenuItem)
def get_menu_item(item_id: str):
    """Get a menu item by ID"""
    item = cafeteria_service.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@app.post("/api/menu", response_model=MenuItem, status_code=status.HTTP_201_CREATED)
def create_menu_item(menu_item: MenuItemCreate):
    """Add a new menu item"""
    return cafeteria_service.create(menu_item)

@app.put("/api/menu/{item_id}", response_model=MenuItem)
def update_menu_item(item_id: str, menu_item: MenuItemUpdate):
    """Update an existing menu item"""
    updated_item = cafeteria_service.update(item_id, menu_item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated_item

@app.delete("/api/menu/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: str):
    """Delete a menu item"""
    success = cafeteria_service.delete(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return None