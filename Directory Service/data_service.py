import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from models import StaffMember

# .env file eke thiyena MongoDB URL eka gannawa
load_dotenv()

class StaffMongoDataService:
    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["university_portal"]
        self.collection = self.db["directory_staff"]

    # MongoDB _id object eka normal string id ekak karanawa
    def format_staff(self, staff_data):
        if staff_data:
            staff_data["id"] = str(staff_data["_id"])
            del staff_data["_id"]
            return staff_data
        return None

    def get_all_staff(self):
        staff_list = []
        for member in self.collection.find():
            staff_list.append(self.format_staff(member))
        return staff_list

    def get_staff_by_id(self, staff_id: str):
        try:
            member = self.collection.find_one({"_id": ObjectId(staff_id)})
            return self.format_staff(member)
        except:
            return None

    def add_staff(self, staff_data):
        staff_dict = staff_data.dict()
        result = self.collection.insert_one(staff_dict)
        return self.get_staff_by_id(str(result.inserted_id))

    def update_staff(self, staff_id: str, staff_data):
        try:
            update_data = staff_data.dict(exclude_unset=True)
            self.collection.update_one(
                {"_id": ObjectId(staff_id)},
                {"$set": update_data}
            )
            return self.get_staff_by_id(staff_id)
        except:
            return None

    def delete_staff(self, staff_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(staff_id)})
            return result.deleted_count > 0
        except:
            return False
