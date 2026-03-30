from database import lost_found_collection
from bson import ObjectId

def item_serializer(item) -> dict:
    return {
        "id": str(item["_id"]),
        "itemName": item["itemName"],
        "description": item["description"],
        "category": item["category"],
        "location": item["location"],
        "reportedBy": item["reportedBy"],
        "contactInfo": item["contactInfo"],
        "type": item["type"],
        "status": item["status"],
        "dateReported": item["dateReported"]
    }

# CREATE
def create_item(data: dict):
    result = lost_found_collection.insert_one(data)
    return lost_found_collection.find_one({"_id": result.inserted_id})

# GET ALL
def get_all_items():
    return [item_serializer(item) for item in lost_found_collection.find()]

# GET LOST
def get_lost_items():
    return [item_serializer(item) for item in lost_found_collection.find({"type": "lost"})]

# GET FOUND
def get_found_items():
    return [item_serializer(item) for item in lost_found_collection.find({"type": "found"})]

# GET BY ID
def get_item_by_id(item_id: str):
    return lost_found_collection.find_one({"_id": ObjectId(item_id)})

# UPDATE
def update_item(item_id: str, data: dict):
    lost_found_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": data}
    )
    return lost_found_collection.find_one({"_id": ObjectId(item_id)})

# DELETE
def delete_item(item_id: str):
    return lost_found_collection.delete_one({"_id": ObjectId(item_id)})

# UPDATE STATUS
def update_status(item_id: str, status: str):
    lost_found_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {"status": status}}
    )
    return lost_found_collection.find_one({"_id": ObjectId(item_id)})