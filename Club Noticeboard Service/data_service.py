import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from models import Notice

load_dotenv()

class NoticeMongoDataService:
    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["university_portal"] 
        self.collection = self.db["club_notices"]  

    def format_notice(self, notice_data):
        if notice_data:
            notice_data["id"] = str(notice_data["_id"])
            del notice_data["_id"]
            return notice_data
        return None

    def get_all_notices(self):
        notices = []
        for notice in self.collection.find():
            notices.append(self.format_notice(notice))
        return notices

    def get_notice_by_id(self, notice_id: str):
        try:
            notice = self.collection.find_one({"_id": ObjectId(notice_id)})
            return self.format_notice(notice)
        except:
            return None

    def add_notice(self, notice_data):
        notice_dict = notice_data.dict()
        result = self.collection.insert_one(notice_dict)
        return self.get_notice_by_id(str(result.inserted_id))

    def update_notice(self, notice_id: str, notice_data):
        try:
            update_data = notice_data.dict(exclude_unset=True)
            self.collection.update_one(
                {"_id": ObjectId(notice_id)}, 
                {"$set": update_data}
            )
            return self.get_notice_by_id(notice_id)
        except:
            return None

    def delete_notice(self, notice_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(notice_id)})
            return result.deleted_count > 0
        except:
            return False