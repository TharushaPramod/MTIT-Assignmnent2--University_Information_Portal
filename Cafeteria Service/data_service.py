import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from models import MenuItem

# Load values from .env file
load_dotenv()

class CafeteriaMongoDataService:
    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["university_portal"]
        self.collection = self.db["cafeteria_menu"]

    # Convert MongoDB _id into normal string id
    def format_menu_item(self, menu_data):
        if menu_data:
            menu_data["id"] = str(menu_data["_id"])
            del menu_data["_id"]
            return menu_data
        return None

    def get_all_menu_items(self):
        menu_items = []
        for item in self.collection.find():
            menu_items.append(self.format_menu_item(item))
        return menu_items

    def get_menu_item_by_id(self, item_id: str):
        try:
            item = self.collection.find_one({"_id": ObjectId(item_id)})
            return self.format_menu_item(item)
        except:
            return None

    def add_menu_item(self, menu_data):
        menu_dict = menu_data.dict()
        result = self.collection.insert_one(menu_dict)
        return self.get_menu_item_by_id(str(result.inserted_id))

    def update_menu_item(self, item_id: str, menu_data):
        try:
            update_data = menu_data.dict(exclude_unset=True)
            self.collection.update_one(
                {"_id": ObjectId(item_id)},
                {"$set": update_data}
            )
            return self.get_menu_item_by_id(item_id)
        except:
            return None

    def delete_menu_item(self, item_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(item_id)})
            return result.deleted_count > 0
        except:
            return False