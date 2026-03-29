from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from routes.menu import router as menu_router
from models.menu_item import MenuItem
import os

load_dotenv()

app = FastAPI(
    title="Cafeteria Service API",
    description="API for managing campus cafeteria menu items - University Information Portal",
    version="1.0.0"
)

# Startup event - connect to MongoDB
@app.on_event("startup")
async def startup_db():
    client = AsyncIOMotorClient(
        os.getenv("MONGO_URI"),
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    await init_beanie(
        database=client.cafeteriadb,
        document_models=[MenuItem]
    )
    print("✅ MongoDB Atlas connected - cafeteriadb")
# Include routes
app.include_router(menu_router, prefix="/menu", tags=["Menu"])

@app.get("/")
def root():
    return {
        "message": "Cafeteria Service is running!",
        "swagger": "http://localhost:3002/docs"
    }