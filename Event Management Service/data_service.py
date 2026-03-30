import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from models import Event

# .env file eke thiyena MONGODB_URI eka load karanawa
load_dotenv()

class EventMongoDataService:
    def __init__(self):
        # Database connection eka hadima
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["university_portal"] # Database eke nama
        self.collection = self.db["events"] # Collection eke nama

    # MongoDB "_id" eka normal "id" string ekak widihata convert karana podi function ekak
    def _serialize_event(self, event_doc):
        if event_doc:
            event_doc["id"] = str(event_doc["_id"])
            del event_doc["_id"]
        return event_doc

    def get_all_events(self):
        # Database eken okkoma events gannawa
        events_cursor = self.collection.find()
        return [self._serialize_event(event) for event in events_cursor]

    def get_event_by_id(self, event_id: str):
        try:
            # ID eken event eka hoyanawa
            event = self.collection.find_one({"_id": ObjectId(event_id)})
            return self._serialize_event(event)
        except Exception:
            # ID format eka waradi nam (Invalid ObjectId)
            return None

    def add_event(self, event_data):
        # Aluth event eka save karanawa
        new_event_dict = event_data.model_dump()
        result = self.collection.insert_one(new_event_dict)
        
        # Save wechcha aluth ID eka gannawa
        new_event_dict["id"] = str(result.inserted_id)
        # return Event(**new_event_dict) # Oyage model eka anuwa mehema return karannath puluwan
        return new_event_dict

    def update_event(self, event_id: str, event_data):
        try:
            update_data = event_data.model_dump(exclude_unset=True)
            if not update_data:
                return self.get_event_by_id(event_id)

            # Database eke data update karanawa
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
            # ID eken event eka delete karanawa
            result = self.collection.delete_one({"_id": ObjectId(event_id)})
            return result.deleted_count > 0
        except Exception:
            return False