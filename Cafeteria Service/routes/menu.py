from fastapi import APIRouter, HTTPException
from models.menu_item import MenuItem
from typing import List

router = APIRouter()

# GET all menu items
@router.get("/", response_model=List[MenuItem])
async def get_all_items():
    items = await MenuItem.find_all().to_list()
    return items

# GET one item by ID
@router.get("/{item_id}")
async def get_item(item_id: str):
    item = await MenuItem.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# POST create new item
@router.post("/", status_code=201)
async def create_item(item: MenuItem):
    await item.insert()
    return item

# PUT update item
@router.put("/{item_id}")
async def update_item(item_id: str, updated: MenuItem):
    item = await MenuItem.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.set(updated.dict(exclude_unset=True))
    return item

# DELETE item
@router.delete("/{item_id}")
async def delete_item(item_id: str):
    item = await MenuItem.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()
    return {"message": "Menu item deleted successfully"}