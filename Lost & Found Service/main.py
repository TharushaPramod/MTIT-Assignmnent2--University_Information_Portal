from fastapi import FastAPI, HTTPException
from schemas import LostFoundItem, UpdateItemModel, UpdateStatusModel
from model import *

app = FastAPI(title="Lost & Found Service")

@app.get("/")
def home():
    return {"message": "Lost & Found Service is running"}

# CREATE
@app.post("/items")
def create(item: LostFoundItem):
    new_item = create_item(item.dict())
    return item_serializer(new_item)

# GET ALL
@app.get("/items")
def get_all():
    return get_all_items()

# GET LOST
@app.get("/items/lost")
def get_lost():
    return get_lost_items()

# GET FOUND
@app.get("/items/found")
def get_found():
    return get_found_items()

# GET BY ID
@app.get("/items/{item_id}")
def get_one(item_id: str):
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_serializer(item)

# UPDATE
@app.put("/items/{item_id}")
def update(item_id: str, data: UpdateItemModel):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    item = update_item(item_id, update_data)
    return item_serializer(item)

# UPDATE STATUS
@app.patch("/items/{item_id}/status")
def update_item_status(item_id: str, status_data: UpdateStatusModel):
    item = update_status(item_id, status_data.status)
    return item_serializer(item)

# DELETE
@app.delete("/items/{item_id}")
def delete(item_id: str):
    delete_item(item_id)
    return {"message": "Item deleted successfully"}