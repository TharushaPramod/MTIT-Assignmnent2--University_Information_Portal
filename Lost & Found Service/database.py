import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get values from .env
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "university_portal")  # Default to 'university_portal' if not set

try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    print("MongoDB Atlas connected successfully")
except Exception as e:
    print("MongoDB connection failed:", e)

db = client[DB_NAME]
lost_found_collection = db["lost_found"]