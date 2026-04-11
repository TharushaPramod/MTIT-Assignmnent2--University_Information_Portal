import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from models import Event

load_dotenv()

class EventMongoDataService:
    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["university_portal"] 
        self.collection = self.db["events"] 

    def _serialize_event(self, event_doc):
        if event_doc:
            event_doc["id"] = str(event_doc["_id"])
            del event_doc["_id"]
        return event_doc

    def get_all_events(self):
        events_cursor = self.collection.find()
        return [self._serialize_event(event) for event in events_cursor]

    def get_event_by_id(self, event_id: str):
        try:
            event = self.collection.find_one({"_id": ObjectId(event_id)})
            return self._serialize_event(event)
        except Exception:
            return None

    def add_event(self, event_data):
        new_event_dict = event_data.model_dump()
        result = self.collection.insert_one(new_event_dict)
        
        new_event_dict["id"] = str(result.inserted_id)
        return new_event_dict

    def update_event(self, event_id: str, event_data):
        try:
            update_data = event_data.model_dump(exclude_unset=True)
            if not update_data:
                return self.get_event_by_id(event_id)

            result = self.collection.update_one(
                {"_id": ObjectId(event_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_event_by_id(event_id)
            return None
        except Exception:
            return None

    def delete_event(self, event_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(event_id)})
            return result.deleted_count > 0
        except Exception:
            return False